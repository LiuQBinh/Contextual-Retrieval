# Scripts

Folder này chứa các script chính để chạy pipeline và các tác vụ khác.

## 📁 Files

### `run_pipeline.py`
Script chính để chạy toàn bộ pipeline chunking.

**Chức năng:**
- Chạy Phase 1: Rough Chunking
- Chạy Phase 2: Agentic Chunking
- Hiển thị tiến trình và kết quả
- Xử lý lỗi và báo cáo

**Cách sử dụng:**
```bash
# Từ thư mục gốc project
python scripts/run_pipeline.py

# Hoặc từ trong folder scripts
cd scripts
python run_pipeline.py
```

## 🚀 Workflow

1. **Khởi động**: Script sẽ tự động tìm project root
2. **Phase 1**: Chạy rough chunking từ PDF files
3. **Phase 2**: Chạy agentic chunking trên chunks thô
4. **Kết quả**: Lưu vào folder `results/`

## 📊 Output

Script sẽ hiển thị:
- Tiến trình từng phase
- Thông báo thành công/lỗi
- Đường dẫn đến kết quả cuối cùng
