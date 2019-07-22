import os
from shutil import copy2

from utils import fs
from core.const import *
from stats.main import get_csv_header
from klee.main import run as klee_run
from angrio.main import run as angr_run
from code.main import compile_code, run_compiled_code


def run(input_path, output_path, stdin, tool, options, credentials):
    input_files_path = fs.ls(input_path, EXT['c'])
    analysis_file_path = os.path.join(output_path, FILE_NAME['analysis'])

    csv_header = get_csv_header(tool)
    fs.write_csv(analysis_file_path, [ csv_header ])

    for input_file_path in input_files_path:
        data = []
        input_file = fs.details(input_file_path)
        input_file_size = os.path.getsize(input_file_path)
        output_dir_path = os.path.join(output_path, input_file['name'])

        fs.mkdir(output_dir_path)
        copy2(input_file_path, output_dir_path) # TODO: Remove file permissions on copy

        if tool == ANGR:
            test_result = angr_run(input_file_path, output_dir_path, stdin, options, credentials)
            data.append([ input_file['file'], input_file_size, str(test_result['time-taken']),
                          str(test_result['is-code-cracked']), str(test_result['is-password-cracked']),
                          test_result['generated-codes'], test_result['generated-passwords'], input_file_path ])

        elif tool == KLEE:
            test_result = klee_run(input_file_path, output_dir_path, stdin, options, credentials)
            data.append([ input_file['file'], input_file_size, str(test_result['time-taken']),
                          str(test_result['is-code-cracked']), str(test_result['is-password-cracked']),
                          test_result['generated-codes'], test_result['generated-passwords'], input_file_path ])

        elif tool == ALL:
            compiled_code_file_path = compile_code(input_file_path, output_dir_path)
            run_test_result = run_compiled_code(compiled_code_file_path, output_dir_path, credentials['codes'],
                                                credentials['passwords'])
            angr_test_result = angr_run(input_file_path, output_dir_path, stdin, options, credentials)
            klee_test_result = klee_run(input_file_path, output_dir_path, stdin, options, credentials)
            data.append([ input_file['file'], input_file_size, str(run_test_result['time-taken']),
                          str(angr_test_result['time-taken']), str(klee_test_result['time-taken']),
                          str(angr_test_result['is-code-cracked']), str(klee_test_result['is-code-cracked']),
                          str(angr_test_result['is-password-cracked']), str(klee_test_result['is-password-cracked']),
                          angr_test_result['generated-codes'], klee_test_result['generated-codes'],
                          angr_test_result['generated-passwords'], klee_test_result['generated-passwords'],
                          input_file_path ])

        fs.append_csv(analysis_file_path, data)
