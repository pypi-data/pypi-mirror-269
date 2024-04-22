import os

def files_in_names(directory, file_names):
    """
    Get the paths of the files with the given names in the directory.
    """
    file_paths = []
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):  # Check if the file exists
            file_paths.append(file_path)
        else:
            print(f"File '{file_name}' not found in directory '{directory}'.")
    return file_paths