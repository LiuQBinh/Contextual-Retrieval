# Streamlit App - Contextual Retrieval Experiment

A Streamlit application for experimenting with Contextual Retrieval based on Anthropic's paper.

## 📁 Directory Structure

```
streamlit_app/
├── app.py        # Main Streamlit application (11.9KB)
└── README.md     # This file
```

## 🚀 Usage

### 1. Install dependencies
```bash
pip install streamlit python-dotenv
```

### 2. Run application
```bash
cd streamlit_app
streamlit run app.py
```

Application will open at: http://localhost:8501

## 🔧 Features

### Tab 1: Setup & Build
- **Load Documents**: Load documents from directory
- **Split Chunks**: Split documents into chunks
- **Generate Context**: Generate context for chunks
- **Build Indices**: Build BM25 and Vector store
- **Save System**: Save system for later use

### Tab 2: Search & Retrieve
- **Load Saved System**: Load previously saved system
- **Search Interface**: Search interface
- **Contextual Retrieval**: Search using context
- **Reranking**: Reorder results

### Tab 3: Evaluation & Comparison
- **Compare Methods**: Compare different methods
- **Performance Metrics**: Evaluate performance
- **Test Queries**: Test queries

## ⚙️ Configuration

### LM Studio
- URL: http://localhost:1234/v1
- Used for LLM and reranking

### Qdrant
- URL: http://localhost:6333
- Vector database

### Parameters
- **Chunk Size**: 200-2000 (default: 800)
- **Chunk Overlap**: 0-500 (default: 200)
- **Top K Results**: 5-50 (default: 20)

## 📊 Workflow

1. **Setup**: Configure LM Studio and Qdrant
2. **Build**: Load documents, split chunks, generate context
3. **Search**: Perform search with different methods
4. **Evaluate**: Compare method performance

## 🎯 Applications

This application is suitable for:
- Contextual Retrieval experiments
- Comparing search method performance
- Retrieval system demos
- Research and development
