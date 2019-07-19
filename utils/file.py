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


def read(path):
    content = ''
    with open(path, 'r') as file:
        content = file.read()

    return content


def write(path, content):
    with open(path, 'w') as file:
        file.write(content)


def lists(path, ext):
    if os.path.isfile(path):
        file = details(path)

        if file['ext'] == ext:
            return [ path ]

    elif os.path.isdir(path):
        file_list = Path(path).glob('**/*{}'.format(ext))

        return [ str(file_path) for file_path in file_list ]

    return []


def remove_dirs_except(path, dir_exception_list = {}):
    dir_list = os.listdir(path)

    for dir in dir_list:
        target_path = os.path.join(path, dir)

        if os.path.isdir(target_path) and dir not in dir_exception_list:
            shutil.rmtree(target_path)


def make_dir_with_parent(path):
    cmd = 'mkdir -p {path}'
    os.system(cmd.format(path = path))
