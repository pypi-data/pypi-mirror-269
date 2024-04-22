import os

def files_in_extension(directory, extension):
    """
    Get the paths of the files with the given extension in the directory.
    """
    file_paths = []
    for file in os.listdir(directory):
        if file.endswith(extension):
            file_path = os.path.join(directory, file)
            file_paths.append(file_path)
    return file_paths