'''Compile and execute c source code.'''
import os

from utils import fs
from utils.time import get_time
from core.const import CMD, FILE_NAME, OPTIONS


def compile_code(input_file_path, output_dir_path, level='0'):
    '''
    Compile c source code using GCC.

    Arguments:
        input_file_path {str} -- C source code file path
        output_dir_path {str} -- C complied code file path

    Keyword Arguments:
        level {str} -- GCC optimization level to compile C source code
                       (default: {'0'})

    Returns:
        str -- File path of compiled c source code
    '''
    input_file = fs.details(input_file_path)
    output_file = FILE_NAME['c-out'].format(
        name=input_file['name'], level=level)
    output_file_path = os.path.join(output_dir_path, output_file)
    gcc = CMD['gcc'].format(
        input=input_file_path,
        output=output_file_path,
        level=level)
    cmd = CMD['bash'].format(gcc)
    os.system(cmd)
    print(gcc)

    return output_file_path


def run_compiled_code(input_path, output_dir_path, args, stdin):
    '''
    Run complied c source code executable.

    Arguments:
        input_path {str} -- File path of compiled c source code
        output_dir_path {str} -- File path to store `time` command output
        args {list} -- Arguments required to run c program
        stdin {list} -- Passwords required to run c program

    Returns:
        float -- [description]
    '''
    input_file = fs.details(input_path)
    run_output_file = FILE_NAME['run'].format(name=input_file['name'])
    run_output_file_path = os.path.join(output_dir_path, run_output_file)

    execute = CMD['run'].format(
        input=input_path,
        args=' '.join(args),
        stdin='\n'.join(stdin))
    time = CMD['time'].format(cmd=execute, output=run_output_file_path)
    cmd = CMD['bash'].format(time)
    output = str(os.popen(cmd).read())
    content = fs.read(run_output_file_path)
    print(output)

    return {
        'time-taken': get_time(content),
    }


def run(input_file_path, output_dir_path, params):
    '''
    Compile c source code and run it.

    Arguments:
        input_file_path {str} -- Path of c source code file
        output_dir_path {str} -- Path to store compiled c source code and
                                 execution time statistics
        params {dict} -- GCC optimization level to compile c source code and
                         arguments, passwords list required to compiled code

    Returns:
        [list] -- Execution time statistics of c program
    '''

    test_results = []

    for level in params['levels']:
        if level in OPTIONS['gcc-optimization-levels']:
            compiled_code_file_path = compile_code(
                input_file_path, output_dir_path, level)
            compiled_code_file_size = os.path.getsize(compiled_code_file_path)
            compiled_code = fs.details(compiled_code_file_path)

            test_result = run_compiled_code(
                compiled_code_file_path,
                output_dir_path,
                params['credentials']['codes'],
                params['credentials']['passwords'])
            test_results.append([compiled_code['file'],
                                 compiled_code_file_size,
                                 level,
                                 test_result['time-taken'],
                                 compiled_code_file_path])

    return test_results
