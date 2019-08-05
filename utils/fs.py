''' Module for file system operations.'''
import os
import csv
import shutil
from pathlib import Path


def details(file_path):
    '''
    Get detials of file.

    Arguments:
        file_path {str} -- Path of file

    Returns:
        dist -- File details
    '''
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
    '''
    Read file content of file.

    Arguments:
        path {str} -- Path of file

    Returns:
        str -- Content of file
    '''
    content = ''
    with open(path, 'r') as file:
        content = file.read()

    return content


def write(path, content):
    '''
    Write to file.

    Arguments:
        path {str} -- Path of file
        content {str} -- Content to write
    '''
    with open(path, 'w') as file:
        file.write(content)


def ls(path, ext):
    '''
    Recursively list files of sepecific extension of a file or a directory.

    Arguments:
        path {str} -- Path of directory or a file
        ext {str} -- File extenion to be listed

    Returns:
        list -- List of files
    '''
    if os.path.isfile(path):
        file = details(path)

        if file['ext'] == ext:
            return [path]

    elif os.path.isdir(path):
        file_list = Path(path).glob('**/*{}'.format(ext))

        return [str(file_path) for file_path in file_list]

    return []


def rmdirs(path, dir_exception_list={}):
    '''
    Delete directories execept from exception lists.

    Arguments:
        path {str} -- Path of direcotry

    Keyword Arguments:
        dir_exception_list {dict} -- List of directories that should not be
                                     deleted (default: {{}})
    '''
    dir_list = os.listdir(path)

    for dir_name in dir_list:
        target_path = os.path.join(path, dir_name)

        if os.path.isdir(target_path) and dir_name not in dir_exception_list:
            shutil.rmtree(target_path)


def find_non_existing_dir(path):
    '''
    Recursively find directory that does not exists.

    Arguments:
        path {str} -- Path of directory

    Returns:
        str -- Path of directory that does not exists
    '''
    if os.path.isdir(path):
        base_path = os.path.dirname(path)
        dir_name = os.path.basename(path)
        dir_index = dir_name.split('-')

        if dir_index[-1].isdigit():
            index = int(dir_index[-1]) + 1
            new_dir_name = '-'.join(dir_index[0:-1]) + '-' + str(index)
        else:
            new_dir_name = dir_name + '-2'

        new_dir_path = os.path.join(base_path, new_dir_name)
        return find_non_existing_dir(new_dir_path)

    return path


def mkdir(path):
    '''
    Make directory with parent.

    Arguments:
        path {str} -- Path of directory

    Returns:
        str -- Path of directory created
    '''
    new_dir_path = find_non_existing_dir(path)
    cmd = 'mkdir -p {path}'.format(path=new_dir_path)
    os.system(cmd)

    return new_dir_path


def write_csv(path, data):
    '''
    Write data to CSV file.

    Arguments:
        path {str} -- Path of file
        data {list} -- Data to write in file
    '''
    with open(path, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def append_csv(path, data):
    '''
    Add data at the end of CSV file.

    Arguments:
        path {str} -- Path of file
        data {list} -- Data to add in file
    '''
    with open(path, 'a') as file:
        writer = csv.writer(file)
        writer.writerows(data)
