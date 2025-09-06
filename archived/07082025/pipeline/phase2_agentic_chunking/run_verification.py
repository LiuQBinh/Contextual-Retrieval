#!/usr/bin/env python3
"""
Simple runner script for chunk quality verification

This script selects 5 random chunks from the previous chunking phase
and applies agentic chunking to verify quality.
"""

import sys
import os
import json
from pathlib import Path
from chunk_quality_verifier import ChunkQualityVerifier

def load_and_display_json_results(json_file: str):
    """Load and display JSON results in a readable format"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n📊 LOADING RESULTS FROM: {json_file}")
        print("=" * 60)
        
        # Display metadata
        if 'metadata' in data:
            metadata = data['metadata']
            print(f"Generated: {metadata.get('generated_at', 'N/A')}")
            print(f"Version: {metadata.get('version', 'N/A')}")
            print(f"Description: {metadata.get('description', 'N/A')}")
            print()
        
        # Display basic info
        print(f"Source file: {data.get('source_file', 'N/A')}")
        print(f"Total chunks available: {data.get('total_chunks_available', 0)}")
        print(f"Chunks tested: {data.get('chunks_tested', 0)}")
        print()
        
        # Display summary
        if 'summary' in data and data['summary']:
            summary = data['summary']
            print("📈 SUMMARY SCORES:")
            print(f"  Average Overall Score: {summary.get('avg_overall_score', 0):.2f}/10")
            print(f"  Average Accuracy Score: {summary.get('avg_accuracy_score', 0):.2f}/10")
            print(f"  Average Coherence Score: {summary.get('avg_coherence_score', 0):.2f}/10")
            print(f"  Average Context Score: {summary.get('avg_context_score', 0):.2f}/10")
            print(f"  Average Logic Score: {summary.get('avg_logic_score', 0):.2f}/10")
            print(f"  Average Added Value Score: {summary.get('avg_added_value_score', 0):.2f}/10")
            print()
        
        # Display individual results
        if 'results' in data and data['results']:
            print("📋 INDIVIDUAL RESULTS:")
            for i, result in enumerate(data['results'], 1):
                chunk = result.get('original_chunk', {})
                assessment = result.get('assessment', {})
                chunk_num = chunk.get('chunk_number', 'N/A')
                overall_score = assessment.get('overall_score', 'N/A')
                feedback = assessment.get('feedback', 'No feedback available')
                
                print(f"  {i}. Chunk {chunk_num}: {overall_score}/10")
                print(f"     Feedback: {feedback[:100]}{'...' if len(feedback) > 100 else ''}")
                print()
        
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {json_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error loading results: {e}")
        return False

def main():
    print("🔍 Chunk Quality Verification")
    print("=" * 50)
    
    # Initialize verifier
    verifier = ChunkQualityVerifier()
    
    # Available chunk files
    chunk_files = {
        "1": "/Users/ggj/Documents/GitHub/Contextual-Retrieval/chunking/chunks_output.txt",
        "2": "/Users/ggj/Documents/GitHub/Contextual-Retrieval/chunking/tang_chi_bo_kinh_chunks.txt"
    }
    
    # Let user choose file or use default
    print("\nAvailable chunk files:")
    for key, file_path in chunk_files.items():
        file_name = Path(file_path).name
        print(f"{key}. {file_name}")
    
    choice = input("\nSelect file (1-2) or press Enter for default (2): ").strip()
    
    if choice in chunk_files:
        selected_file = chunk_files[choice]
    else:
        selected_file = chunk_files["2"]  # Default
    
    print(f"\n✅ Using: {Path(selected_file).name}")
    
    # Ask for number of chunks
    num_chunks_input = input("\nNumber of chunks to verify (default 5): ").strip()
    try:
        num_chunks = int(num_chunks_input) if num_chunks_input else 5
    except ValueError:
        num_chunks = 5
    
    print(f"📊 Will verify {num_chunks} random chunks")
    print("💾 Results will be automatically saved to JSON files")
    
    # Check if LM Studio is running
    print("\n🔄 Checking LM Studio connection...")
    test_response = verifier.agentic_chunker.call_lm_studio("Test connection")
    if not test_response:
        print("❌ Cannot connect to LM Studio at http://localhost:1234")
        print("Please make sure LM Studio is running and has a model loaded.")
        return 1
    
    print("✅ LM Studio connection successful")
    
    # Run verification
    print(f"\n🚀 Starting verification process...")
    print(f"This will take several minutes depending on model speed...")
    
    try:
        results = verifier.run_verification(selected_file, num_chunks)
        
        if results:
            # Save results with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"verification_results_{timestamp}.json"
            report_file = f"verification_report_{timestamp}.txt"
            
            # Also save to default files for easy access
            default_results_file = "verification_results.json"
            default_report_file = "verification_report.txt"
            
            verifier.save_verification_results(results, results_file)
            verifier.save_verification_results(results, default_results_file)
            verifier.save_verification_report(results, report_file)
            verifier.save_verification_report(results, default_report_file)
            
            print(f"\n✅ Verification completed successfully!")
            print(f"📄 Full results saved to: {results_file}")
            print(f"📄 Full results also saved to: {default_results_file}")
            print(f"📄 Summary results saved to: {results_file.replace('.json', '_summary.json')}")
            print(f"📄 Summary results also saved to: {default_results_file.replace('.json', '_summary.json')}")
            print(f"📄 Human-readable report saved to: {report_file}")
            print(f"📄 Human-readable report also saved to: {default_report_file}")
            
            # Show detailed summary
            if 'summary' in results and results['summary']:
                summary = results['summary']
                avg_score = summary.get('avg_overall_score', 0)
                print(f"\n📊 DETAILED SUMMARY")
                print(f"Average Overall Score: {avg_score:.2f}/10")
                print(f"Average Accuracy Score: {summary.get('avg_accuracy_score', 0):.2f}/10")
                print(f"Average Coherence Score: {summary.get('avg_coherence_score', 0):.2f}/10")
                print(f"Average Context Score: {summary.get('avg_context_score', 0):.2f}/10")
                print(f"Average Logic Score: {summary.get('avg_logic_score', 0):.2f}/10")
                print(f"Average Added Value Score: {summary.get('avg_added_value_score', 0):.2f}/10")
                
                if avg_score >= 8:
                    print("🟢 Excellent chunking quality!")
                elif avg_score >= 6:
                    print("🟡 Good chunking quality")
                elif avg_score >= 4:
                    print("🟠 Fair chunking quality - needs improvement")
                else:
                    print("🔴 Poor chunking quality - significant improvements needed")
            
            # Show individual results summary
            if 'results' in results and results['results']:
                print(f"\n📋 INDIVIDUAL RESULTS")
                for i, result in enumerate(results['results'], 1):
                    assessment = result.get('assessment', {})
                    overall_score = assessment.get('overall_score', 'N/A')
                    chunk_num = result.get('original_chunk', {}).get('chunk_number', 'N/A')
                    print(f"  Chunk {chunk_num}: {overall_score}/10")
            
            # Show how to view JSON results
            print(f"\n💡 To view detailed JSON results:")
            print(f"   cat {default_results_file}")
            print(f"   cat {default_results_file.replace('.json', '_summary.json')}")
        else:
            print("❌ Verification failed - no results generated")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Verification cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
