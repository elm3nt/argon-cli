import os

def details(file_path):
    path = os.path.dirname(str(file_path))
    file = os.path.basename(str(file_path))
    name, ext = os.path.splitext(file)

    return {
        'ext': ext,
        'name': name,
        'path': path,
        'file': file,
    }
