import os
from shutil import copy2

from utils import fs
from core.const import *
from stats.main import get_csv_header
from klee.main import run as klee_run
from angrio.main import run as angr_run
from code.main import compile_code, run_compiled_code


def get_credentials(credentials):
    result = []
    if len(credentials):
        result += ['\n'.join(str(e) for e in credentials)]

    return result


def extract_codes(test_result, codes):
    result = []
    if len(codes):
        result += [test_result['is-code-cracked'],
                   test_result['generated-codes']]

    return result


def extract_passwords(test_result, passwords):
    result = []
    if len(passwords):
        result += [test_result['is-password-cracked'],
                   test_result['generated-passwords']]

    return result


def angr(input_file_path, output_dir_path, params):
    test_result = angr_run(
        input_file_path,
        output_dir_path,
        params['stdin'],
        params['options'],
        params['credentials'])

    result = [test_result['time-taken']]
    result += get_credentials(params['credentials']['codes'])
    result += extract_codes(test_result, params['credentials']['codes'])
    result += get_credentials(params['credentials']['passwords'])
    result += extract_passwords(test_result,
                                params['credentials']['passwords'])

    return result


def klee(input_file_path, output_dir_path, params):
    test_result = klee_run(
        input_file_path,
        output_dir_path,
        params['stdin'],
        params['options'],
        params['credentials'])

    result = [test_result['time-taken']]
    result += get_credentials(params['credentials']['codes'])
    result += extract_codes(test_result, params['credentials']['codes'])
    result += get_credentials(params['credentials']['passwords'])
    result += extract_passwords(test_result,
                                params['credentials']['passwords'])

    return result


def all(input_file_path, output_dir_path, params):
    compiled_code_file_path = compile_code(input_file_path, output_dir_path)
    run_test_result = run_compiled_code(
        compiled_code_file_path,
        output_dir_path,
        params['credentials']['codes'],
        params['credentials']['passwords'])
    klee_test_result = klee_run(
        input_file_path,
        output_dir_path,
        params['stdin'],
        params['options'],
        params['credentials'])
    angr_test_result = angr_run(
        input_file_path,
        output_dir_path,
        params['stdin'],
        params['options'],
        params['credentials'])

    result = [
        run_test_result['time-taken'],
        angr_test_result['time-taken'],
        klee_test_result['time-taken']]
    result += get_credentials(params['credentials']['codes'])
    result += extract_codes(angr_test_result, params['credentials']['codes'])
    result += extract_codes(klee_test_result, params['credentials']['codes'])
    result += get_credentials(params['credentials']['passwords'])
    result += extract_passwords(angr_test_result,
                                params['credentials']['passwords'])
    result += extract_passwords(klee_test_result,
                                params['credentials']['passwords'])

    return result


def run(input_file_path, output_dir_path, params):
    input_file = fs.details(input_file_path)
    input_file_size = os.path.getsize(input_file_path)

    if params['tool'] == ANGR:
        test_results = angr(input_file_path, output_dir_path, params)

    elif params['tool'] == KLEE:
        test_results = klee(input_file_path, output_dir_path, params)

    elif params['tool'] == ALL:
        test_results = all(input_file_path, output_dir_path, params)

    return [[input_file['file'], input_file_size] +
            test_results + [input_file_path]]
