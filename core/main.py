'''Project core module.'''
import os
from shutil import copy2

from utils import fs
from core.const import EXT, FILE_NAME
from stats.main import get_csv_header


def file_iterator(input_path, output_path, tool, func_name, func_args):
    """
    Recursively iterate c files from a given path. Call given function on each
    file.

    Arguments:
        input_path {str} -- Input path of source files
        output_path {str} -- Output path to store test results
        tool {str} -- Tool to run on each file iteration
        func_name {str} -- Name of function to call in each iternation
        func_args {dict} -- Arguments requried for function call
    """
    input_files_path = fs.ls(input_path, EXT['c'])
    new_output_path = fs.mkdir(output_path)

    csv_header = get_csv_header(tool, func_args['credentials'])
    analysis_file_path = os.path.join(new_output_path, FILE_NAME['analysis'])
    fs.write_csv(analysis_file_path, [csv_header])

    for input_file_path in input_files_path:
        input_file = fs.details(input_file_path)
        output_dir_path = os.path.join(new_output_path, input_file['name'])
        new_output_dir_path = fs.mkdir(output_dir_path)
        # TODO: Remove file permissions on copy
        copy2(input_file_path, new_output_dir_path)

        test_results = func_name(input_file_path, new_output_dir_path, func_args)
        fs.append_csv(analysis_file_path, test_results)
