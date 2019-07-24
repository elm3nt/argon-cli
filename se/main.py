import os
from shutil import copy2

from utils import fs
from core.const import *
from stats.main import get_csv_header
from klee.main import run as klee_run
from angrio.main import run as angr_run
from code.main import compile_code, run_compiled_code


def angr(input_file_path, output_dir_path, params):
    test_result = angr_run(input_file_path, output_dir_path, params['stdin'], params['options'],
                            params['credentials'])

    return [ str(test_result['time-taken']), str(test_result['is-code-cracked']),
             str(test_result['is-password-cracked']), test_result['generated-codes'],
             test_result['generated-passwords'] ]


def klee(input_file_path, output_dir_path, params):
    test_result = klee_run(input_file_path, output_dir_path, params['stdin'], params['options'],
                            params['credentials'])

    return [ str(test_result['time-taken']), str(test_result['is-code-cracked']),
             str(test_result['is-password-cracked']), test_result['generated-codes'],
             test_result['generated-passwords'] ]


def all(input_file_path, output_dir_path, params):
    compiled_code_file_path = compile_code(input_file_path, output_dir_path)
    run_test_result = run_compiled_code(compiled_code_file_path, output_dir_path, params['credentials']['codes'],
                                        params['credentials']['passwords'])
    klee_test_result = klee_run(input_file_path, output_dir_path, params['stdin'], params['options'],
                                params['credentials'])
    angr_test_result = angr_run(input_file_path, output_dir_path, params['stdin'], params['options'],
                                params['credentials'])

    return [ str(run_test_result['time-taken']), str(angr_test_result['time-taken']),
             str(klee_test_result['time-taken']), str(angr_test_result['is-code-cracked']),
             str(klee_test_result['is-code-cracked']), str(angr_test_result['is-password-cracked']),
             str(klee_test_result['is-password-cracked']), angr_test_result['generated-codes'],
             klee_test_result['generated-codes'], angr_test_result['generated-passwords'],
             klee_test_result['generated-passwords'] ]


def run(input_file_path, output_dir_path, params):
    input_file = fs.details(input_file_path)
    input_file_size = os.path.getsize(input_file_path)

    if params['tool'] == ANGR:
        test_results = angr(input_file_path, output_dir_path, params)

    elif params['tool'] == KLEE:
        test_results = klee(input_file_path, output_dir_path, params)

    elif params['tool'] == ALL:
        test_results = all(input_file_path, output_dir_path, params)

    return [ [ input_file['file'], input_file_size ] + test_results + [ input_file_path ] ]
