'''Module to run sybolic execution.'''
import os

from utils import fs
from klee.main import run as klee_run
from core.const import ANGR, KLEE, ALL
from angrio.main import run as angr_run
from code.main import compile_code, run_compiled_code


def get_credentials(credentials):
    '''
    Get credentials by joining with new line.

    Arguments:
        credentials {list} -- Credentials in list

    Returns:
        list -- List of credentials joined by new line
    '''
    result = []
    if credentials:
        result += ['\n'.join(str(e) for e in credentials)]

    return result


def extract_codes(test_result, codes):
    '''
    Extract activation codes from test results if activation codes is provided.

    Arguments:
        test_result {dict} -- Test result of activation codes
        codes {list} -- Activation codes required to run the program

    Returns:
        list -- Test result of activation codes
    '''
    result = []
    if codes:
        result += [test_result['is-code-cracked'],
                   test_result['generated-codes']]

    return result


def extract_passwords(test_result, passwords):
    '''
    Extract passwords from test results if passwords is provided.

    Arguments:
        test_result {dict} -- Test result of passwords
        codes {list} -- Passwords required to run the program

    Returns:
        list -- Test result of passwords
    '''
    result = []
    if passwords:
        result += [test_result['is-password-cracked'],
                   test_result['generated-passwords']]

    return result


def angr(input_file_path, output_dir_path, params):
    '''
    Run symbolic execution using Angr and extract test results.

    Arguments:
        input_file_path {str} -- Path of executable file
        output_dir_path {str} -- Path to store test results
        params {dict} -- Parameters required to run symbolic execution

    Returns:
        dict -- Test results of symbolic execution
    '''
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
    '''
    Run symbolic execution using Klee and extract test results.

    Arguments:
        input_file_path {str} -- Path of executable file
        output_dir_path {str} -- Path to store test results
        params {dict} -- Parameters required to run symbolic execution

    Returns:
        dict -- Test results of symbolic execution
    '''
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


def run_all(input_file_path, output_dir_path, params):
    '''
    Run symbolic execution and note execution time to run compiled c program.
    Use Angr and Klee to run symbolic execution using and then extract
    test results.

    Arguments:
        input_file_path {str} -- Path of executable file
        output_dir_path {str} -- Path to store test results
        params {dict} -- Parameters required to run symbolic execution

    Returns:
        dict -- Test results of symbolic execution
    '''
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
    '''
    Run symbolic exection or compiled c program or both.

    Arguments:
        input_file_path {str} -- Path of input file
        output_dir_path {str} -- Path to store test results
        params {dict} -- Paramters required to run symbolic exectution or
                         compiled c program or both.

    Returns:
        dict -- Test results
    '''
    input_file = fs.details(input_file_path)
    input_file_size = os.path.getsize(input_file_path)

    if params['tool'] == ANGR:
        test_results = angr(input_file_path, output_dir_path, params)

    elif params['tool'] == KLEE:
        test_results = klee(input_file_path, output_dir_path, params)

    elif params['tool'] == ALL:
        test_results = run_all(input_file_path, output_dir_path, params)

    return [[input_file['file'], input_file_size] +
            test_results + [input_file_path]]
