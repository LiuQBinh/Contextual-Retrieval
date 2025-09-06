import os

# Simplest way to read files from folder and append to array
def read_files_to_array(folder_path):
    files_array = []
    
    # Walk through all files and subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_array.append(file_path)
    
    return files_array

# Usage
folder = "corpus"
files_array = read_files_to_array(folder)

print(f"Read {len(files_array)} files from folder '{folder}':")
for i, file in enumerate(files_array, 1):
    print(f"{i}. {file}")

# Now you can use files_array to do something else
print(f"\nArray files_array has {len(files_array)} elements")
print("You can access the first file with: files_array[0]")
print("You can iterate through all files using a for loop")
