# Contextual Retrieval - Chunking Pipeline

Project này thực hiện việc chunking văn bản kinh Phật qua pipeline 2 phases để tạo ra dữ liệu chất lượng cao cho việc retrieval.

## 🏗️ Cấu trúc Project

```
Contextual-Retrieval/
├── corpus/                           # Chứa các file PDF gốc
│   ├── tang-chi-bo-kinh/            # Tăng Chi Bộ Kinh
│   └── tuong-ung-bo-kinh/           # Tương Ưng Bộ Kinh
├── pipeline/                         # Pipeline xử lý
│   ├── phase1_rough_chunking/       # Phase 1: Chunking thô
│   └── phase2_agentic_chunking/     # Phase 2: Chunking thông minh
├── results/                          # Kết quả pipeline
│   ├── phase1_rough_chunks.txt      # Chunks thô từ Phase 1
│   └── phase2_agentic_chunks.txt    # Chunks chất lượng cao từ Phase 2
├── file_readers/                     # Module đọc file
├── scripts/                          # Scripts chính
│   └── run_pipeline.py              # Script chạy toàn bộ pipeline
└── results/                          # Kết quả pipeline
```

## 🚀 Cách sử dụng

### Chạy toàn bộ pipeline
```bash
python scripts/run_pipeline.py
```

### Chạy từng phase riêng lẻ

#### Phase 1: Rough Chunking
```bash
cd pipeline/phase1_rough_chunking
python run_tang_chi.py
```

#### Phase 2: Agentic Chunking
```bash
cd pipeline/phase2_agentic_chunking
python run_agentic_chunking.py
```

## 📋 Mô tả Pipeline

### Phase 1: Rough Chunking
- **Input**: PDF files từ corpus
- **Process**: Chunking thô văn bản thành các mẫu kinh nhỏ
- **Output**: `results/phase1_rough_chunks.txt`
- **Technology**: AGNO library

### Phase 2: Agentic Chunking
- **Input**: Chunks thô từ Phase 1
- **Process**: Sử dụng AI agent để chunking thông minh
- **Output**: `results/phase2_agentic_chunks.txt`
- **Technology**: AI agent với LM Studio

## 🔧 Dependencies

Cài đặt dependencies cho từng phase:

```bash
# Phase 1
cd pipeline/phase1_rough_chunking
pip install -r requirements.txt

# Phase 2
cd ../phase2_agentic_chunking
pip install -r requirements.txt
```

## 📊 Kết quả

Pipeline sẽ tạo ra 2 file kết quả:
- **`phase1_rough_chunks.txt`**: Chunks thô, dễ đọc
- **`phase2_agentic_chunks.txt`**: Chunks chất lượng cao, được tối ưu hóa

## 🎯 Ứng dụng

- Xử lý văn bản kinh Phật
- Chuẩn bị dữ liệu cho AI/ML
- Phân tích văn bản theo cấu trúc tự nhiên
- Pipeline chunking tự động hóa
- Tạo dữ liệu chất lượng cao cho retrieval systems
