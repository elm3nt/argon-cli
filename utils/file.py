import os
import shutil
from pathlib import Path


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

def list(path, ext):
    if os.path.isfile(path):
        file = details(path)

        if file['ext'] == ext:
            return [ path ]

    elif os.path.isdir(path):
        file_list = Path(path).glob('**/*{}'.format(ext))

        return [ str(file_path) for file_path in file_list ]

    return []

def clean_up(path):
    shutil.rmtree(path) #TODO: Fix file permissions
    os.mkdir(path)

