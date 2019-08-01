import os
from shutil import copy2

from utils import fs
from core.const import *
from stats.main import get_csv_header


def file_iterator(input_path, output_path, tool, fn, fn_args):
    input_files_path = fs.ls(input_path, EXT['c'])
    new_output_path = fs.mkdir(output_path)

    csv_header = get_csv_header(tool, fn_args['credentials'])
    analysis_file_path = os.path.join(new_output_path, FILE_NAME['analysis'])
    fs.write_csv(analysis_file_path, [ csv_header ])

    for input_file_path in input_files_path:
        input_file = fs.details(input_file_path)
        output_dir_path = os.path.join(new_output_path, input_file['name'])
        new_output_dir_path = fs.mkdir(output_dir_path)
        copy2(input_file_path, new_output_dir_path) # TODO: Remove file permissions on copy

        test_results = fn(input_file_path, new_output_dir_path, fn_args)
        fs.append_csv(analysis_file_path, test_results)
