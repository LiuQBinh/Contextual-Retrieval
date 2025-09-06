import os
import json
import random
import logging
from typing import List, Dict, Any, Tuple
from pathlib import Path
from agentic_chunker import AgenticChunker

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('verification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ChunkQualityVerifier:
    def __init__(self, api_url: str = "http://localhost:1234/v1"):
        self.agentic_chunker = AgenticChunker(api_url)
        
    def parse_chunks_file(self, chunk_file_path: str) -> List[Dict[str, Any]]:
        """Parse chunks from the previous chunking phase"""
        chunks = []
        
        try:
            with open(chunk_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split by chunk separator
            chunk_sections = content.split('================================================================================')
            
            for i, section in enumerate(chunk_sections[1:], 1):  # Skip header
                if not section.strip():
                    continue
                    
                lines = section.strip().split('\n')
                chunk_info = {}
                chunk_content = []
                
                # Parse chunk metadata
                for line in lines:
                    if line.startswith('CHUNK '):
                        chunk_info['chunk_number'] = line.split('/')[0].replace('CHUNK ', '')
                        chunk_info['total_chunks'] = line.split('/')[1]
                    elif line.startswith('Length: '):
                        chunk_info['length'] = line.replace('Length: ', '').replace(' characters', '')
                    elif line.startswith('--------------------------------------------------'):
                        # Content starts after this line
                        start_idx = lines.index(line) + 1
                        chunk_content = lines[start_idx:]
                        break
                
                if chunk_content:
                    chunk_info['content'] = '\n'.join(chunk_content)
                    chunk_info['original_index'] = i
                    chunks.append(chunk_info)
                    
        except Exception as e:
            logger.error(f"Error parsing chunks file: {e}")
            
        return chunks
    
    def select_random_chunks(self, chunks: List[Dict[str, Any]], num_chunks: int = 5) -> List[Dict[str, Any]]:
        """Select random chunks for verification"""
        if len(chunks) < num_chunks:
            logger.warning(f"Only {len(chunks)} chunks available, selecting all")
            return chunks
            
        selected = random.sample(chunks, num_chunks)
        logger.info(f"Selected {len(selected)} random chunks for verification")
        return selected
    
    def apply_agentic_chunking(self, chunk: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply agentic chunking to a single chunk"""
        logger.info(f"Applying agentic chunking to chunk {chunk['chunk_number']}")
        
        content = chunk['content']
        chunk_index = int(chunk['chunk_number'])
        
        # Use agentic chunker to process this content
        agentic_chunks = self.agentic_chunker.process_text_chunk(content, chunk_index)
        
        return agentic_chunks
    
    def create_quality_assessment_prompt(self, original_chunk: Dict[str, Any], 
                                       agentic_chunks: List[Dict[str, Any]]) -> str:
        """Create prompt for quality assessment"""
        
        agentic_text = "\n".join([f"- [{chunk['context']}], {chunk['content']}" 
                                for chunk in agentic_chunks])
        
        prompt = f"""
Bạn là chuyên gia đánh giá chất lượng chunking văn bản kinh Phật. Hãy so sánh giữa chunk gốc và kết quả agentic chunking.

CHUNK GỐC:
{original_chunk['content']}

AGENTIC CHUNKING KẾT QUẢ:
{agentic_text}

Hãy đánh giá theo các tiêu chí sau (thang điểm 1-10):

1. TÍNH CHÍNH XÁC (Accuracy): Agentic chunks có bảo toàn đầy đủ nội dung gốc không?
2. TÍNH MẠCH LẠC (Coherence): Các chunks có ý nghĩa hoàn chỉnh và liên kết không?
3. NGỮ CẢNH (Context): Thông tin ngữ cảnh có phù hợp và hữu ích không?
4. TÍNH LOGIC (Logic): Cách chia chunks có logic và dễ hiểu không?
5. GIÁ TRỊ THÊM (Added Value): Agentic chunking có mang lại giá trị gì so với chunk gốc?

Trả về kết quả theo format JSON:
{{
  "accuracy_score": <điểm 1-10>,
  "coherence_score": <điểm 1-10>,
  "context_score": <điểm 1-10>,
  "logic_score": <điểm 1-10>,
  "added_value_score": <điểm 1-10>,
  "overall_score": <điểm trung bình>,
  "feedback": "<nhận xét chi tiết>",
  "strengths": ["<điểm mạnh 1>", "<điểm mạnh 2>"],
  "improvements": ["<cần cải thiện 1>", "<cần cải thiện 2>"]
}}
"""
        return prompt
    
    def assess_quality(self, original_chunk: Dict[str, Any], 
                      agentic_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess the quality of agentic chunking"""
        prompt = self.create_quality_assessment_prompt(original_chunk, agentic_chunks)
        
        response = self.agentic_chunker.call_lm_studio(prompt)
        
        try:
            # Try to parse JSON response
            import json
            assessment = json.loads(response)
            return assessment
        except:
            # If JSON parsing fails, create basic assessment
            logger.warning("Failed to parse assessment JSON, creating basic assessment")
            return {
                "accuracy_score": 5,
                "coherence_score": 5, 
                "context_score": 5,
                "logic_score": 5,
                "added_value_score": 5,
                "overall_score": 5,
                "feedback": response,
                "strengths": [],
                "improvements": ["Assessment parsing failed"]
            }
    
    def run_verification(self, chunk_file_path: str, num_chunks: int = 5) -> Dict[str, Any]:
        """Run complete verification workflow"""
        logger.info(f"Starting chunk quality verification with {num_chunks} random chunks")
        
        # Parse existing chunks
        chunks = self.parse_chunks_file(chunk_file_path)
        logger.info(f"Parsed {len(chunks)} chunks from file")
        
        if not chunks:
            logger.error("No chunks found in file")
            return {}
        
        # Select random chunks
        selected_chunks = self.select_random_chunks(chunks, num_chunks)
        
        verification_results = {
            "source_file": chunk_file_path,
            "total_chunks_available": len(chunks),
            "chunks_tested": len(selected_chunks),
            "results": [],
            "summary": {}
        }
        
        all_scores = {
            "accuracy_scores": [],
            "coherence_scores": [],
            "context_scores": [],
            "logic_scores": [],
            "added_value_scores": [],
            "overall_scores": []
        }
        
        # Process each selected chunk
        for i, chunk in enumerate(selected_chunks, 1):
            logger.info(f"Processing chunk {i}/{len(selected_chunks)}: Chunk {chunk['chunk_number']}")
            
            try:
                # Apply agentic chunking
                agentic_chunks = self.apply_agentic_chunking(chunk)
                
                if not agentic_chunks:
                    logger.warning(f"No agentic chunks generated for chunk {chunk['chunk_number']}")
                    continue
                
                # Assess quality
                assessment = self.assess_quality(chunk, agentic_chunks)
                
                result = {
                    "original_chunk": chunk,
                    "agentic_chunks": agentic_chunks,
                    "assessment": assessment
                }
                
                verification_results["results"].append(result)
                
                # Collect scores for summary
                for score_type in all_scores.keys():
                    score_key = score_type.replace('_scores', '_score')
                    if score_key in assessment:
                        all_scores[score_type].append(assessment[score_key])
                
                logger.info(f"Completed chunk {chunk['chunk_number']} - Overall score: {assessment.get('overall_score', 'N/A')}")
                
            except Exception as e:
                logger.error(f"Error processing chunk {chunk['chunk_number']}: {e}")
                continue
        
        # Calculate summary statistics
        if verification_results["results"]:
            summary = {}
            for score_type, scores in all_scores.items():
                if scores:
                    summary[f"avg_{score_type.replace('_scores', '_score')}"] = sum(scores) / len(scores)
                    summary[f"min_{score_type.replace('_scores', '_score')}"] = min(scores)
                    summary[f"max_{score_type.replace('_scores', '_score')}"] = max(scores)
            
            verification_results["summary"] = summary
            logger.info(f"Verification complete. Average overall score: {summary.get('avg_overall_score', 'N/A')}")
        
        return verification_results
    
    def save_verification_results(self, results: Dict[str, Any], output_file: str):
        """Save verification results to JSON file with enhanced formatting"""
        from datetime import datetime
        
        # Add metadata to results
        enhanced_results = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0",
                "description": "Chunk Quality Verification Results"
            },
            **results
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(enhanced_results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Verification results saved to {output_file}")
            
            # Also save a summary-only version for quick reference
            summary_file = output_file.replace('.json', '_summary.json')
            summary_data = {
                "metadata": enhanced_results["metadata"],
                "source_file": results.get("source_file", ""),
                "total_chunks_available": results.get("total_chunks_available", 0),
                "chunks_tested": results.get("chunks_tested", 0),
                "summary": results.get("summary", {}),
                "quick_stats": {
                    "avg_overall_score": results.get("summary", {}).get("avg_overall_score", 0),
                    "total_results": len(results.get("results", [])),
                    "successful_assessments": len([r for r in results.get("results", []) if r.get("assessment", {}).get("overall_score")])
                }
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Summary results saved to {summary_file}")
            
        except Exception as e:
            logger.error(f"Error saving verification results: {e}")
            raise
    
    def save_verification_report(self, results: Dict[str, Any], output_file: str):
        """Save human-readable verification report"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("CHUNK QUALITY VERIFICATION REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Source file: {results['source_file']}\n")
            f.write(f"Total chunks available: {results['total_chunks_available']}\n")
            f.write(f"Chunks tested: {results['chunks_tested']}\n\n")
            
            # Summary
            if 'summary' in results and results['summary']:
                f.write("SUMMARY SCORES\n")
                f.write("-" * 40 + "\n")
                summary = results['summary']
                f.write(f"Average Overall Score: {summary.get('avg_overall_score', 'N/A'):.2f}\n")
                f.write(f"Average Accuracy Score: {summary.get('avg_accuracy_score', 'N/A'):.2f}\n")
                f.write(f"Average Coherence Score: {summary.get('avg_coherence_score', 'N/A'):.2f}\n")
                f.write(f"Average Context Score: {summary.get('avg_context_score', 'N/A'):.2f}\n")
                f.write(f"Average Logic Score: {summary.get('avg_logic_score', 'N/A'):.2f}\n")
                f.write(f"Average Added Value Score: {summary.get('avg_added_value_score', 'N/A'):.2f}\n\n")
            
            # Individual results
            for i, result in enumerate(results['results'], 1):
                f.write(f"VERIFICATION RESULT {i}\n")
                f.write("=" * 80 + "\n")
                
                chunk = result['original_chunk']
                f.write(f"Original Chunk: {chunk['chunk_number']}\n")
                f.write(f"Length: {chunk['length']} characters\n\n")
                
                f.write("ORIGINAL CONTENT:\n")
                f.write("-" * 20 + "\n")
                f.write(f"{chunk['content'][:500]}...\n\n")
                
                f.write(f"AGENTIC CHUNKS ({len(result['agentic_chunks'])}):\n")
                f.write("-" * 20 + "\n")
                for j, agentic_chunk in enumerate(result['agentic_chunks'], 1):
                    f.write(f"{j}. [{agentic_chunk['context']}]\n")
                    f.write(f"   {agentic_chunk['content'][:200]}...\n\n")
                
                assessment = result['assessment']
                f.write("ASSESSMENT:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Overall Score: {assessment.get('overall_score', 'N/A')}\n")
                f.write(f"Accuracy: {assessment.get('accuracy_score', 'N/A')}\n")
                f.write(f"Coherence: {assessment.get('coherence_score', 'N/A')}\n")
                f.write(f"Context: {assessment.get('context_score', 'N/A')}\n")
                f.write(f"Logic: {assessment.get('logic_score', 'N/A')}\n")
                f.write(f"Added Value: {assessment.get('added_value_score', 'N/A')}\n\n")
                
                f.write(f"Feedback: {assessment.get('feedback', 'N/A')}\n\n")
                
                if assessment.get('strengths'):
                    f.write("Strengths:\n")
                    for strength in assessment['strengths']:
                        f.write(f"- {strength}\n")
                    f.write("\n")
                
                if assessment.get('improvements'):
                    f.write("Areas for Improvement:\n")
                    for improvement in assessment['improvements']:
                        f.write(f"- {improvement}\n")
                    f.write("\n")
                
                f.write("=" * 80 + "\n\n")
        
        logger.info(f"Verification report saved to {output_file}")

def main():
    """Main function to run chunk quality verification"""
    verifier = ChunkQualityVerifier()
    
    # Available chunk files
    chunk_files = [
        "/Users/ggj/Documents/GitHub/Contextual-Retrieval/chunking/chunks_output.txt",
        "/Users/ggj/Documents/GitHub/Contextual-Retrieval/chunking/tang_chi_bo_kinh_chunks.txt"
    ]
    
    # Select which file to use
    chunk_file = chunk_files[1]  # Use tang_chi_bo_kinh_chunks.txt by default
    
    logger.info(f"Using chunk file: {chunk_file}")
    
    # Run verification
    results = verifier.run_verification(chunk_file, num_chunks=5)
    
    if results:
        # Save results
        results_file = "verification_results.json"
        report_file = "verification_report.txt"
        
        verifier.save_verification_results(results, results_file)
        verifier.save_verification_report(results, report_file)
        
        logger.info("Verification completed successfully!")
    else:
        logger.error("Verification failed - no results generated")

if __name__ == "__main__":
    main()
