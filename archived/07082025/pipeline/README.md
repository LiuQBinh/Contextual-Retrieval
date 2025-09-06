# Pipeline Chunking

Pipeline này thực hiện việc chunking văn bản qua 2 phases:

## Phase 1: Rough Chunking
- **Mục đích**: Chunking thô văn bản thành các mẫu kinh nhỏ
- **Input**: PDF files từ corpus
- **Output**: Chunks thô được lưu vào `results/phase1_rough_chunks.txt`
- **Module**: `phase1_rough_chunking/`

## Phase 2: Agentic Chunking
- **Mục đích**: Chunking thông minh sử dụng AI agent
- **Input**: Chunks thô từ Phase 1
- **Output**: Chunks chất lượng cao được lưu vào `results/phase2_agentic_chunks.txt`
- **Module**: `phase2_agentic_chunking/`

## Cách sử dụng

1. Chạy Phase 1:
```bash
cd phase1_rough_chunking
python run_tang_chi.py
```

2. Chạy Phase 2:
```bash
cd phase2_agentic_chunking
python run_agentic_chunking.py
```

## Kết quả
Tất cả kết quả sẽ được lưu trong folder `results/`:
- `phase1_rough_chunks.txt`: Kết quả chunking thô
- `phase2_agentic_chunks.txt`: Kết quả chunking thông minh
