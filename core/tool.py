import os
from shutil import copy2

from utils import file
from core.const import *
from klee.main import run as klee_run
from angrio.main import run as angr_run
from stats.main import get_csv_header, write_to_file


def run(input_path, output_path, stdin, tool, options, credentials):
    input_files_path = file.lists(input_path, C_EXT)
    csv_header = get_csv_header(tool)
    data = [ csv_header ]

    for input_file_path in input_files_path:
        input_file = file.details(input_file_path)
        input_file_size = os.path.getsize(input_file_path)
        output_dir_path = os.path.join(output_path, input_file['name'])

        os.mkdir(output_dir_path)
        copy2(input_file_path, output_dir_path) # TODO: Remove file permissions on copy

        # if tool == EXECUTION:
        #     test_result = klee_run(input_file_path, output_dir_path, stdin, options, credentials)
        #     data.append([ input_file['file'], input_file_size, test_result['execution-time'], input_file_path ])

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
            angr_test_result = angr_run(input_file_path, output_dir_path, stdin, options, credentials)
            klee_test_result = klee_run(input_file_path, output_dir_path, stdin, options, credentials)
            data.append([ input_file['file'], input_file_size, str(angr_test_result['time-taken']),
                          str(klee_test_result['time-taken']), str(angr_test_result['is-code-cracked']),
                          str(klee_test_result['is-code-cracked']), str(angr_test_result['is-password-cracked']),
                          str(klee_test_result['is-password-cracked']), angr_test_result['generated-codes'],
                          klee_test_result['generated-codes'], angr_test_result['generated-passwords'],
                          klee_test_result['generated-passwords'], input_file_path ])

    analysis_file_path = os.path.join(output_path, FILE_NAME['analysis'])
    write_to_file(analysis_file_path, data)




        # elif tool == KLEE:
        #     test_result = klee_run(input_file_path, output_dir_path, stdin, options, credentials)
        #     data.append([input_file['file'], '', str(test_result['time']), input_file_size, input_file_path])

        # elif tool == SYMBOLIC_EXECUTION or tool == SE:
        #     angr_test_result = angr_run(input_file_path, output_dir_path, stdin, options, credentials)
        #     klee_test_result = klee_run(input_file_path, output_dir_path, stdin, options, credentials)
        #     data.append([input_file['file'], str(angr_test_result['time']), str(klee_test_result['time']),
        #                  input_file_size, input_file_path])
