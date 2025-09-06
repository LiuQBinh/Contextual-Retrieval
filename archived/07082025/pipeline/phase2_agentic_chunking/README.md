# Phase 2: Agentic Chunking

Phase này thực hiện việc chunking thông minh sử dụng AI agent để tạo ra các chunks chất lượng cao.

## Chức năng
- Nhận input từ chunks thô của Phase 1
- Sử dụng AI agent để phân tích và chunking thông minh
- Lưu kết quả vào `results/phase2_agentic_chunks.txt`

## Files chính
- `agentic_chunker.py`: Module chunking thông minh chính
- `chunk_quality_verifier.py`: Module kiểm tra chất lượng chunks
- `config.py`: Cấu hình cho agentic chunking
- `requirements.txt`: Dependencies cần thiết

## Cách sử dụng
```bash
python run_agentic_chunking.py
```

## Input
Chunks thô từ Phase 1 (file `results/phase1_rough_chunks.txt`)

## Output
Kết quả chunking thông minh sẽ được lưu vào `results/phase2_agentic_chunks.txt`
