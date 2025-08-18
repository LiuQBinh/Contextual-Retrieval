# PDF Chunking System

A PDF chunking system using AGNO approach to split PDF files into chunks by story structure.

## 📁 Directory Structure

```
chunking/
├── agno_chunking.py      # Main chunking script
├── chunks_output.txt     # Output containing all chunks
├── chunking.log         # Detailed log file
└── README.md           # This file
```

## 🚀 Usage

### 1. Install dependencies
```bash
pip install pypdf pdfplumber langchain
```

### 2. Run script
```bash
cd chunking
python agno_chunking.py
```

## 📊 Results

### Statistics:
- **Source file**: `corpus/tang-chi-bo-kinh/09_CHƯƠNG_IX:_CHƯƠNG_CHÍN_PHÁP.pdf`
- **Chunks created**: 71 chunks
- **Chunk sizes**: 68 to 20,290 characters each

### Quality:
- ✅ Remove PDF noise (lines like "Page X of Y")
- ✅ Chunk by story structure (sutras) instead of fixed size
- ✅ Each story is a separate chunk
- ✅ Clean text, no extra whitespace

## 🔧 Features

### 1. PDF Text Extraction
- Use `pdfplumber` for high-quality text extraction
- Remove PDF noise

### 2. Text Cleaning
- Remove "Page X of Y" lines
- Remove lines containing only page numbers
- Remove extra blank lines

### 3. Story-based Chunking
- Find title patterns: `(Roman) (Number) Title`
- Find opening patterns: `Thus I have heard:` (Vietnamese: `Như vầy tôi nghe:`)
- Each story is a separate chunk

### 4. Detailed Logging
- Log processing steps
- Chunk statistics
- Information about each chunk size

## 📝 Output

### chunks_output.txt
Contains all 71 chunks with format:
```
==================================================
CHUNK X/71
Length: Y characters
==================================================
Content:
[Story title]
[Story content]
```

### chunking.log
Detailed processing log including:
- File processing information
- Character count before and after cleaning
- Number of chunks created
- Processing time

## 🎯 Applications

This system is suitable for:
- Buddhist document processing
- Natural structure chunking
- AI/ML data preparation
- Text analysis by story structure
