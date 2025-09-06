# Phase 1: Rough Chunking

Phase này thực hiện việc chunking thô văn bản PDF thành các mẫu kinh nhỏ.

## Chức năng
- Đọc file PDF từ corpus
- Chunking văn bản thành các đoạn nhỏ
- Lưu kết quả vào `results/phase1_rough_chunks.txt`

## Files chính
- `agno_chunking.py`: Module chunking sử dụng agno library
- `run_tang_chi.py`: Script chính để chạy chunking
- `requirements.txt`: Dependencies cần thiết

## Cách sử dụng
```bash
python run_tang_chi.py
```

## Output
Kết quả chunking thô sẽ được lưu vào `results/phase1_rough_chunks.txt`
