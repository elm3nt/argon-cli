import os

from utils import fs
from core.const import *
from utils.time import get_time


def compile_code(input_file_path, output_dir_path):
    input_file = fs.details(input_file_path)
    output_file = FILE_NAME['c-out'].format(name = input_file['name'])
    output_file_path = os.path.join(output_dir_path, output_file)
    gcc = CMD['gcc'].format(input = input_file_path, output = output_file_path)
    cmd = CMD['bash'].format(gcc)
    os.system(cmd)

    return output_file_path


def run_compiled_code(input_path, output_dir_path, args, stdin):
    input_file = fs.details(input_path)
    run_output_file = FILE_NAME['run'].format(name = input_file['name'])
    run_output_file_path = os.path.join(output_dir_path, run_output_file)

    execute = CMD['run'].format(input = input_path, args = ' '.join(args), stdin = '\n'.join(stdin))
    time = CMD['time'].format(cmd = execute, output = run_output_file_path)
    cmd = CMD['bash'].format(time)
    output = str(os.popen(cmd).read())
    print(output)

    content = fs.read(run_output_file_path)

    return {
        'time-taken': get_time(content),
    }


