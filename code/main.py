import os
from shutil import copy2

from utils import fs
from core.const import *
from utils.time import get_time
from stats.main import get_csv_header


def compile_code(input_file_path, output_dir_path, level='0'):
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
