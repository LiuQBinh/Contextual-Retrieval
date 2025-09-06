import os
import json
import logging
from typing import List, Dict, Any
from pathlib import Path
import requests
from config import LM_STUDIO_CONFIG, LOGGING_CONFIG, CHUNKING_CONFIG, get_lm_studio_url, get_api_endpoint

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG["log_file"]),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AgenticChunker:
    def __init__(self, api_url: str = None):
        self.api_url = api_url or get_lm_studio_url()
        
    def call_lm_studio(self, prompt: str, model: str = None) -> str:
        """Gọi LM Studio để chunking"""
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model or LM_STUDIO_CONFIG["model"],
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": LM_STUDIO_CONFIG["temperature"],
                "max_tokens": LM_STUDIO_CONFIG["max_tokens"],
                "stream": LM_STUDIO_CONFIG["stream"]
            }
            
            endpoint = get_api_endpoint("chat_completions")
            response = requests.post(endpoint, json=payload, headers=headers, timeout=LM_STUDIO_CONFIG["timeout"])
            response.raise_for_status()
            
            result = response.json()
            return result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            
        except Exception as e:
            logger.error(f"Lỗi khi gọi LM Studio: {e}")
            return ""
    
    def create_chunking_prompt(self, text: str, chunk_index: int) -> str:
        """Tạo prompt cho semantic chunking"""
        prompt = f"""
Bạn là chuyên gia phân tích và chunking văn bản kinh Phật. Hãy đọc và hiểu đoạn văn bản sau, sau đó thực hiện semantic chunking.

YÊU CẦU:
1. Hiểu toàn bộ câu chuyện và bối cảnh
2. Tách ý nghĩa thành các chunk có ý nghĩa hoàn chỉnh
3. Giữ nguyên text gốc
4. Thêm ngữ cảnh cho mỗi chunk theo format: [ngữ cảnh], [nội dung chunk]
5. Chỉ trả lời output là chunk, không cần giải thích thêm
6. Trả lời bằng tiếng Việt

VĂN BẢN CẦN CHUNKING (Chunk {chunk_index}):
{text}

Hãy thực hiện semantic chunking và trả về kết quả theo format:
[ngữ cảnh], [nội dung chunk]
"""
        return prompt
    
    def process_text_chunk(self, text: str, chunk_index: int) -> List[Dict[str, Any]]:
        """Xử lý một chunk text với LM Studio"""
        logger.info(f"Đang xử lý chunk {chunk_index}")
        
        prompt = self.create_chunking_prompt(text, chunk_index)
        response = self.call_lm_studio(prompt)
        
        if not response:
            logger.warning(f"Không nhận được phản hồi cho chunk {chunk_index}")
            return []
        
        # Debug: in ra response
        logger.info(f"Response từ LM Studio: {response[:500]}...")
        
        # Parse response thành các chunk
        chunks = self.parse_chunking_response(response, chunk_index)
        logger.info(f"Parse được {len(chunks)} chunks")
        return chunks
    
    def parse_chunking_response(self, response: str, original_chunk_index: int) -> List[Dict[str, Any]]:
        """Parse response từ LM Studio thành các chunk có cấu trúc"""
        chunks = []
        lines = response.strip().split('\n')

        chunk_counter = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Tìm pattern [ngữ cảnh], nội dung
            if line.startswith('[') and '], ' in line:
                try:
                    # Tách ngữ cảnh và nội dung
                    parts = line.split('], ', 1)  # Split chỉ 1 lần
                    if len(parts) == 2:
                        context = parts[0][1:]  # Bỏ dấu [
                        content = parts[1]
                        
                        chunk_data = {
                            "chunk_id": f"{original_chunk_index}_{chunk_counter}",
                            "original_chunk": original_chunk_index,
                            "sub_chunk": chunk_counter,
                            "context": context,
                            "content": content,
                            "full_text": line
                        }
                        chunks.append(chunk_data)
                        chunk_counter += 1
                        
                except Exception as e:
                    logger.error(f"Lỗi parse line: {line}, error: {e}")
                    continue
        
        return chunks
    
    def read_pdf(self, pdf_path: str) -> str:
        """Đọc file PDF và trả về text"""
        try:
            import pdfplumber
            
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            return text
        except Exception as e:
            logger.error(f"Lỗi đọc PDF {pdf_path}: {str(e)}")
            return ""
    
    def process_pdf_file(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Xử lý toàn bộ file PDF"""
        logger.info(f"Bắt đầu xử lý file: {pdf_path}")
        
        # Đọc PDF
        text_content = self.read_pdf(pdf_path)
        if not text_content:
            logger.error(f"Không thể đọc file: {pdf_path}")
            return []
        
        # Chia thành các chunk lớn trước (để tránh quá tải)
        large_chunks = self.split_into_large_chunks(text_content)
        
        all_chunks = []
        for i, large_chunk in enumerate(large_chunks, 1):
            logger.info(f"Xử lý large chunk {i}/{len(large_chunks)}")
            
                    # Gửi từng large chunk cho LM Studio
        semantic_chunks = self.process_text_chunk(large_chunk, i)
        all_chunks.extend(semantic_chunks)
        
        # Log progress
        logger.info(f"Đã xử lý {len(semantic_chunks)} semantic chunks từ large chunk {i}")
        
        return all_chunks
    
    def split_into_large_chunks(self, text: str, max_chars: int = None) -> List[str]:
        """Chia text thành các chunk lớn để gửi cho GPT OSS"""
        if max_chars is None:
            max_chars = CHUNKING_CONFIG["max_chars_per_chunk"]
        
        chunks = []
        current_chunk = ""
        
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) > max_chars:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    # Paragraph quá dài, chia nhỏ hơn
                    words = paragraph.split()
                    temp_chunk = ""
                    for word in words:
                        if len(temp_chunk) + len(word) + 1 > max_chars:
                            if temp_chunk:
                                chunks.append(temp_chunk.strip())
                                temp_chunk = word
                            else:
                                # Word quá dài, cắt
                                chunks.append(word[:max_chars])
                        else:
                            temp_chunk += " " + word if temp_chunk else word
                    current_chunk = temp_chunk
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def save_chunks(self, chunks: List[Dict[str, Any]], output_file: str):
        """Lưu chunks ra file JSON"""
        output_data = {
            "total_chunks": len(chunks),
            "chunks": chunks
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Đã lưu {len(chunks)} chunks vào {output_file}")
    
    def save_chunks_text(self, chunks: List[Dict[str, Any]], output_file: str):
        """Lưu chunks ra file text để dễ đọc"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Tổng số chunks: {len(chunks)}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, chunk in enumerate(chunks, 1):
                f.write(f"CHUNK {i}/{len(chunks)}\n")
                f.write(f"ID: {chunk['chunk_id']}\n")
                f.write(f"Ngữ cảnh: {chunk['context']}\n")
                f.write("-" * 50 + "\n")
                f.write(f"{chunk['content']}\n")
                f.write("=" * 80 + "\n\n")
        
        logger.info(f"Đã lưu chunks text vào {output_file}")

def main():
    """Hàm chính để chạy agentic chunking"""
    chunker = AgenticChunker()
    
    # Thư mục corpus - sử dụng absolute path
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    corpus_dir = project_root / "corpus"
    
    # Tạo thư mục output
    output_dir = Path(CHUNKING_CONFIG["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Xử lý từng file PDF trong corpus
    for pdf_dir in corpus_dir.iterdir():
        if pdf_dir.is_dir():
            logger.info(f"Xử lý thư mục: {pdf_dir.name}")
            
            for pdf_file in pdf_dir.glob("*.pdf"):
                logger.info(f"Đang xử lý file: {pdf_file.name}")
                
                try:
                    # Xử lý file
                    chunks = chunker.process_pdf_file(str(pdf_file))
                    
                    if chunks:
                        # Tạo tên file output
                        base_name = pdf_file.stem
                        json_output = output_dir / f"{base_name}_agentic_chunks.json"
                        text_output = output_dir / f"{base_name}_agentic_chunks.txt"
                        
                        # Lưu kết quả
                        chunker.save_chunks(chunks, str(json_output))
                        chunker.save_chunks_text(chunks, str(text_output))
                        
                        logger.info(f"Hoàn thành xử lý {pdf_file.name}: {len(chunks)} chunks")
                    else:
                        logger.warning(f"Không tạo được chunks cho {pdf_file.name}")
                        
                except Exception as e:
                    logger.error(f"Lỗi xử lý {pdf_file.name}: {e}")
                    continue

if __name__ == "__main__":
    main()
