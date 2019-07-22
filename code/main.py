import os
from shutil import copy2

from utils import fs
from core.const import *
from utils.time import get_time
from stats.main import get_csv_header


def compile_code(input_file_path, output_dir_path, level = '0'):
    input_file = fs.details(input_file_path)
    output_file = FILE_NAME['c-out'].format(name = input_file['name'], level = level)
    output_file_path = os.path.join(output_dir_path, output_file)
    gcc = CMD['gcc'].format(input = input_file_path, output = output_file_path, level = level)
    cmd = CMD['bash'].format(gcc)
    os.system(cmd)
    print(gcc)

    return output_file_path


def run_compiled_code(input_path, output_dir_path, args, stdin):
    input_file = fs.details(input_path)
    run_output_file = FILE_NAME['run'].format(name = input_file['name'])
    run_output_file_path = os.path.join(output_dir_path, run_output_file)

    execute = CMD['run'].format(input = input_path, args = ' '.join(args), stdin = '\n'.join(stdin))
    time = CMD['time'].format(cmd = execute, output = run_output_file_path)
    cmd = CMD['bash'].format(time)
    output = str(os.popen(cmd).read())
    content = fs.read(run_output_file_path)
    print(output)

    return {
        'time-taken': get_time(content),
    }



def run(input_path, output_path, optimization_levels, credentials):
    input_files_path = fs.ls(input_path, EXT['c'])
    analysis_file_path = os.path.join(output_path, FILE_NAME['analysis'])

    csv_header = get_csv_header(RUN)
    fs.write_csv(analysis_file_path, [ csv_header ])
    for input_file_path in input_files_path:
        input_file = fs.details(input_file_path)
        output_dir_path = os.path.join(output_path, input_file['name'])

        fs.mkdir(output_dir_path)
        copy2(input_file_path, output_dir_path) # TODO: Remove file permissions on copy

        for level in optimization_levels:
            if level in OPTIONS['gcc-optimization-levels']:
                data = []
                compiled_code_file_path = compile_code(input_file_path, output_dir_path, level)
                compiled_code_file_size = os.path.getsize(compiled_code_file_path)
                compiled_code = fs.details(compiled_code_file_path)
                test_result = run_compiled_code(compiled_code_file_path, output_dir_path, credentials['codes'],
                                                    credentials['passwords'])

                data.append([ compiled_code['file'], compiled_code_file_size, level, test_result['time-taken'],
                              compiled_code_file_path ])
                fs.append_csv(analysis_file_path, data)
