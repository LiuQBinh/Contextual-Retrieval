import os

def get_files_from_folder(folder_path):
    """
    Simple function to read all files from folder and append to array
    """
    files_array = []
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return files_array
    
    # Walk through all files in folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            files_array.append(file_path)
    
    return files_array

def get_files_recursive(folder_path):
    """
    Function to read files recursively from folder and all subfolders
    """
    files_array = []
    
    # Walk through all files and subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_array.append(file_path)
    
    return files_array

# Usage
if __name__ == "__main__":
    # Read files from corpus folder
    folder = "corpus"
    
    print("=== Method 1: Read files directly from folder ===")
    files = get_files_from_folder(folder)
    print(f"Found {len(files)} files:")
    for file in files:
        print(f"  {file}")
    
    print("\n=== Method 2: Read files recursively (including subfolders) ===")
    all_files = get_files_recursive(folder)
    print(f"Found {len(all_files)} files (including subfolders):")
    for file in all_files:
        print(f"  {file}")
    
    # Save to array for use
    my_files_array = all_files
    print(f"\nSaved {len(my_files_array)} files to array 'my_files_array'")
