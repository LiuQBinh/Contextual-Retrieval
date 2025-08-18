import os
from pathlib import Path

def read_files_from_folder(folder_path, file_extensions=None):
    """
    Read file list from folder and append to array
    
    Args:
        folder_path (str): Path to folder to read
        file_extensions (list): List of extensions to filter (e.g., ['.pdf', '.txt'])
    
    Returns:
        list: List of found files
    """
    file_list = []
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist!")
        return file_list
    
    # Walk through all files and directories in folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # If extension filter is provided
            if file_extensions:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in file_extensions:
                    file_list.append(file_path)
            else:
                # If no filter, get all files
                file_list.append(file_path)
    
    return file_list

def read_files_recursive(folder_path, file_extensions=None):
    """
    Use pathlib to read files recursively
    
    Args:
        folder_path (str): Path to folder to read
        file_extensions (list): List of extensions to filter
    
    Returns:
        list: List of found files
    """
    file_list = []
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Folder {folder_path} does not exist!")
        return file_list
    
    # Find all files in folder and subfolders
    if file_extensions:
        for ext in file_extensions:
            files = folder.rglob(f"*{ext}")
            file_list.extend([str(f) for f in files])
    else:
        files = folder.rglob("*")
        file_list = [str(f) for f in files if f.is_file()]
    
    return file_list

# Usage example
if __name__ == "__main__":
    # Path to corpus folder
    corpus_folder = "corpus"
    
    print("=== Read all files in corpus folder ===")
    all_files = read_files_from_folder(corpus_folder)
    print(f"Total files found: {len(all_files)}")
    for file in all_files:
        print(f"  - {file}")
    
    print("\n=== Read only PDF files in corpus folder ===")
    pdf_files = read_files_from_folder(corpus_folder, ['.pdf'])
    print(f"Total PDF files found: {len(pdf_files)}")
    for file in pdf_files:
        print(f"  - {file}")
    
    print("\n=== Using pathlib (recursive) ===")
    pdf_files_pathlib = read_files_recursive(corpus_folder, ['.pdf'])
    print(f"Total PDF files found: {len(pdf_files_pathlib)}")
    for file in pdf_files_pathlib:
        print(f"  - {file}")
    
    # Save file list to array for later use
    file_array = pdf_files
    print(f"\nSaved {len(file_array)} files to array for use")
