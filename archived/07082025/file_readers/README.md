# File Readers Collection

A collection of scripts to read files from folders and append to arrays.

## 📁 Directory Structure

```
file_readers/
├── example_usage.py        # Simplest approach (917B)
├── simple_file_reader.py   # Simple version with multiple options (1.8KB)
├── file_reader.py         # Full-featured version (3.1KB)
└── README.md             # This file
```

## 🚀 Usage

### 1. example_usage.py - Simplest Approach
```bash
cd file_readers
python example_usage.py
```
**Features:**
- Read all files from folder and subfolders
- Simple array append
- Print file list

### 2. simple_file_reader.py - Simple Version
```bash
cd file_readers
python simple_file_reader.py
```
**Features:**
- Read files directly from folder
- Recursive file reading (including subfolders)
- Compare two methods

### 3. file_reader.py - Full-featured Version
```bash
cd file_readers
python file_reader.py
```
**Features:**
- Filter by extension (e.g., PDF only)
- Use pathlib for better performance
- Multiple file reading methods
- Better error handling

## 📊 Version Comparison

| Version | Size | Features | Complexity |
|---------|------|----------|------------|
| example_usage.py | 917B | Basic | ⭐ |
| simple_file_reader.py | 1.8KB | Medium | ⭐⭐ |
| file_reader.py | 3.1KB | Full | ⭐⭐⭐ |

## 🎯 Applications

These scripts are suitable for:
- Reading file lists from directories
- Data preparation for processing
- Integration into larger systems
- Learning and reference
