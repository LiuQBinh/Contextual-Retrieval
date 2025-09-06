import os
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chunking.log'),
        logging.StreamHandler()
    ]
)

def read_files_to_array(folder_path):
    """Read file list from folder and append to array"""
    files_array = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_array.append(file_path)
    
    return files_array

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file using pdfplumber"""
    try:
        import pdfplumber
        
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        return text
    except Exception as e:
        logging.error(f"Error reading PDF {pdf_path}: {str(e)}")
        return ""

def clean_pdf_text(text):
    """Clean text from PDF, remove noise"""
    import re
    
    # Remove "Page X of Y" lines
    text = re.sub(r'Page \d+of \d+\n?', '', text)
    
    # Remove lines containing only page numbers
    text = re.sub(r'^\d+$\n?', '', text, flags=re.MULTILINE)
    
    # Remove extra blank lines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Remove extra whitespace at beginning and end
    text = text.strip()
    
    return text

def chunk_by_stories(text):
    """
    Chunking by story structure (sutras) - each story is a chunk
    Based on:
      - Opening line: 'Thus I have heard:' (Vietnamese: 'Như vầy tôi nghe:')
      - Or title format: '(VI) (37) Venerable Ananda' (Vietnamese: 'Tôn Giả Ananda')
    """
    stories = []
    import re
    # Title pattern: (Roman) (Number) Title
    title_pattern = r"^\s*\(\s*[IVXLCDM]+\s*\)\s*\(\s*\d+\s*\)\s+.+$"
    # Opening pattern: '1. - Thus I have heard:' or '1. Thus I have heard:'
    opening_pattern = r"^\s*\d+\.\s*(?:-\s*)?Như vầy tôi nghe:"
    combined_pattern = rf"{title_pattern}|{opening_pattern}"
    title_matches = list(re.finditer(title_pattern, text, flags=re.MULTILINE))
    opening_matches = list(re.finditer(opening_pattern, text, flags=re.MULTILINE))
    # Prioritize cutting by title; only fallback to 'Thus I have heard:' when no titles
    split_matches = title_matches if title_matches else opening_matches
    logging.info(
        f"Titles found: {len(title_matches)} | Openings found: {len(opening_matches)} | Used for splitting: {len(split_matches)}"
    )
    if not split_matches:
        return [text.strip()] if text.strip() else []
    # Cut according to selected milestone list
    for index, match in enumerate(split_matches):
        start_pos = match.start()
        end_pos = split_matches[index + 1].start() if index + 1 < len(split_matches) else len(text)
        story = text[start_pos:end_pos].strip()
        if story:
            stories.append(story)
            logging.info(f"Story {len(stories)}: {len(story)} characters")
    return stories

def process_pdf_file(pdf_path, output_file='chunks_output.txt'):
    """
    Process a specific PDF file and create chunks
    
    Args:
        pdf_path (str): Path to the PDF file to process
        output_file (str): Output file name for chunks (default: 'chunks_output.txt')
    
    Returns:
        list: List of text chunks
    """
    logging.info(f"Processing PDF file: {pdf_path}")
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        logging.error(f"File not found: {pdf_path}")
        return []
    
    # Extract text from PDF
    logging.info("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text.strip():
        logging.error("Could not extract text from PDF")
        return []
    
    logging.info(f"Extracted {len(text)} characters from PDF")
    
    # Clean text, remove noise
    logging.info("Cleaning text, removing noise...")
    cleaned_text = clean_pdf_text(text)
    logging.info(f"After cleaning: {len(cleaned_text)} characters")
    
    # Use story-based chunking
    logging.info("Performing story-based chunking...")
    chunks = chunk_by_stories(cleaned_text)
    
    logging.info(f"Created {len(chunks)} chunks")
    
    # Log each chunk
    for i, chunk in enumerate(chunks, 1):
        logging.info(f"\n{'='*50}")
        logging.info(f"CHUNK {i}/{len(chunks)}")
        logging.info(f"Length: {len(chunk)} characters")
        logging.info(f"{'='*50}")
        logging.info(f"Content:\n{chunk}")
        logging.info(f"{'='*50}\n")
    
    # Save chunks to file for easy viewing
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Source file: {pdf_path}\n")
        f.write(f"Total chunks: {len(chunks)}\n")
        f.write("="*80 + "\n\n")
        
        for i, chunk in enumerate(chunks, 1):
            f.write(f"CHUNK {i}/{len(chunks)}\n")
            f.write(f"Length: {len(chunk)} characters\n")
            f.write("-"*50 + "\n")
            f.write(chunk)
            f.write("\n" + "="*80 + "\n\n")
    
    logging.info(f"Saved chunks to file '{output_file}'")
    logging.info(f"Saved log to file 'chunking.log'")
    
    return chunks

def main():
    # Read file list
    folder = "corpus"
    files_array = read_files_to_array(folder)
    
    if not files_array:
        logging.error("No files found in folder")
        return
    
    # Get first file
    first_file = files_array[0]
    logging.info(f"Processing first file: {first_file}")
    
    # Process the file
    chunks = process_pdf_file(first_file)
    
    if chunks:
        logging.info(f"Successfully processed {len(chunks)} chunks")

if __name__ == "__main__":
    main()
