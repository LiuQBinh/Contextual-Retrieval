#!/usr/bin/env python3
"""
Script to run chunking on Tang Chi Bo Kinh PDF
"""

import sys
import os

# Add current directory to path to import agno_chunking
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agno_chunking import process_pdf_file

def main():
    # Path to the Tang Chi Bo Kinh PDF
    pdf_path = "/Users/ggj/Documents/GitHub/Contextual-Retrieval/corpus/tang-chi-bo-kinh.pdf"
    
    # Output file name - save to results folder
    output_file = "/Users/ggj/Documents/GitHub/Contextual-Retrieval/results/phase1_rough_chunks.txt"
    
    print(f"Starting chunking process for: {pdf_path}")
    print(f"Output will be saved to: {output_file}")
    print("-" * 60)
    
    # Process the PDF file
    chunks = process_pdf_file(pdf_path, output_file)
    
    if chunks:
        print(f"\n✅ Successfully processed {len(chunks)} chunks")
        print(f"📄 Results saved to: {output_file}")
        print(f"📋 Log saved to: chunking.log")
    else:
        print("\n❌ Failed to process the PDF file")
        print("Check the log file for details")

if __name__ == "__main__":
    main()
