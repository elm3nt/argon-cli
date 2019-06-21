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


def get_time(content):
    hour =  re.search(r'real\t(.*?)h(.*?)m(.*?)s', content)
    if hour:
        hh = int(hour.group(1))

        min_sec = re.search(r'real\t[\d]*h(.*?)m(.*?)s', content)
        if min_sec:
            mm = int(min_sec.group(1))
            ss = int(min_sec.group(2).split('.')[0])
            ms = int(min_sec.group(2).split('.')[1])

            return (hh * 3600) + (mm * 60) + ss + (ms / 1000)

    else:
        min_sec = re.search(r'real\t(.*?)m(.*?)s', content)
        if min_sec:
            mm = int(min_sec.group(1))
            ss = int(min_sec.group(2).split('.')[0])
            ms = int(min_sec.group(2).split('.')[1])

            return (mm * 60) + ss + (ms / 1000)

    return '#error'


def time_taken(output_path, file_name):
    log_file = FILE_NAME['log'].format(name = file_name)
    log_file_path = os.path.join(output_path, log_file)

    time = '#error'
    with open(log_file_path, 'r') as log_file:
        content = log_file.read()
        time = get_time(content)

    return time


def run(input_file_path, output_dir_path, stdin, options):
    input_file = file.details(input_file_path)
    bytecode_file = FILE_NAME['bytecode'].format(name = input_file['name'])
    bytecode_file_path = os.path.join(output_dir_path, bytecode_file)

    compile(input_file_path, bytecode_file_path)

    symbolic_execution(output_dir_path, stdin, input_file['name'], bytecode_file_path, options)

    time = time_taken(output_dir_path, input_file['name'])

    return {
        'time': time
    }
