# Contextual Retrieval Project

A comprehensive project for experimenting with Contextual Retrieval, including file reading tools, PDF chunking, and Streamlit application.

## 📁 Project Structure

```
Contextual-Retrieval/
├── chunking/              # PDF Chunking System
│   ├── agno_chunking.py
│   ├── chunks_output.txt
│   ├── chunking.log
│   └── README.md
├── file_readers/          # File Readers Collection
│   ├── example_usage.py
│   ├── simple_file_reader.py
│   ├── file_reader.py
│   └── README.md
├── streamlit_app/         # Streamlit Application
│   ├── app.py
│   └── README.md
├── corpus/                # Data directory
│   ├── tang-chi-bo-kinh/
│   └── tuong-ung-bo-kinh/
└── README.md             # This file
```

## 🚀 Quick Start

### 1. File Readers (Read files from folder)
```bash
cd file_readers
python example_usage.py
```

### 2. PDF Chunking (Split PDF into chunks)
```bash
cd chunking
python agno_chunking.py
```

### 3. Streamlit App (Web application)
```bash
cd streamlit_app
streamlit run app.py
```

## 📊 Component Overview

### 🔧 File Readers Collection
- **example_usage.py**: Simplest way to read files
- **simple_file_reader.py**: Version with multiple options
- **file_reader.py**: Full-featured version

**Features:**
- Read files from folders and subfolders
- Filter by extension
- Append to array
- Error handling

### ✂️ PDF Chunking System
- **agno_chunking.py**: Main PDF chunking script
- **chunks_output.txt**: Output containing 71 chunks
- **chunking.log**: Detailed process log

**Features:**
- Extract text from PDF using pdfplumber
- Remove noise (lines like "Page X of Y")
- Chunk by story structure (sutras)
- Each story is a separate chunk

### 🌐 Streamlit Application
- **app.py**: Complete web application

**Features:**
- Setup & Build system
- Search & Retrieve
- Evaluation & Comparison
- Contextual Retrieval
- Reranking

## 🛠️ Dependencies

### File Readers
```bash
# No special dependencies required
```

### PDF Chunking
```bash
pip install pypdf pdfplumber langchain
```

### Streamlit App
```bash
pip install streamlit python-dotenv
```

## 📈 Achievements

### File Readers
- ✅ 3 different versions for different needs
- ✅ Good error handling
- ✅ Easy to use and integrate

### PDF Chunking
- ✅ 71 high-quality chunks from PDF file
- ✅ Completely remove noise
- ✅ Chunking by natural structure
- ✅ Clean text, no extra whitespace

### Streamlit App
- ✅ User-friendly web interface
- ✅ 3 functional tabs
- ✅ LM Studio and Qdrant integration
- ✅ Performance comparison of methods

## 🎯 Applications

This project is suitable for:
- **Research**: Contextual Retrieval, RAG systems
- **Development**: Building intelligent search systems
- **Learning**: Understanding chunking, retrieval, vector search
- **Demo**: Showcasing AI/ML capabilities

## 📝 Notes

- All components have their own detailed README
- Code is organized in clear modules
- Easy to extend and integrate
- Suitable for both beginners and experienced users
