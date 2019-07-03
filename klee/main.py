import os
import re
import sys
import shutil

from .const import *
from utils import file
from core.const import *
from pathlib import Path


def compile(input_file_path, output_file_path):
    cmd = KLEE_CMD['compile'].format(input = input_file_path, output = output_file_path)
    os.system(CMD['bash'].format(cmd))


def symbolic_execution(output_path, stdin, file_name, bytecode_file_path, options):
    log_file = FILE_NAME['log'].format(name = file_name)
    log_file_path = os.path.join(output_path, log_file)
    output_dir = os.path.join(output_path, file_name)

    sym_args = ''
    if (stdin['num-arg'] >= 1):
        sym_args = KLEE_CMD['sym-args'].format(max = str(stdin['num-arg']), length = str(stdin['length-arg']))

    sym_stdin = ''
    if (stdin['num-input'] >= 1):
        sym_stdin = KLEE_CMD['sym-stdin'].format(length = str(stdin['length-input']))

    cmd = KLEE_CMD['options'].format(input = bytecode_file_path, output = output_dir, memory = str(options['memory']),
                                 time = str(options['timeout']), search = options['search'], file = log_file_path,
                                 sym_args = sym_args, sym_stdin = sym_stdin)
    os.system(CMD['bash'].format(cmd))


def time_taken(input_path):
    time = 0
    cmd = KLEE_CMD['stats'].format(input = input_path)
    content = os.popen(cmd).read()

    seconds =  re.search(r'[\s]*[\d]*\.[\d]*', str(content))
    if seconds:
        time = float(seconds.group(0).strip())

    return time

def run(input_file_path, output_dir_path, stdin, options):
    input_file = file.details(input_file_path)
    bytecode_file = FILE_NAME['bytecode'].format(name = input_file['name'])
    bytecode_file_path = os.path.join(output_dir_path, bytecode_file)

    compile(input_file_path, bytecode_file_path)
    symbolic_execution(output_dir_path, stdin, input_file['name'], bytecode_file_path, options)

    return {
        'time': time_taken(output_dir_path)
    }
