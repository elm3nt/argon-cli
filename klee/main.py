#!/usr/bin/python3

import os
import sys
import shutil
from .const import *
from core.const import *
from pathlib import Path

def compile(test_path, c_file_path, c_file_name, bytecode_file_path):
        compile = COMPILE['compile'].format(input = c_file_path, output = bytecode_file_path)
        os.system(CMD['bash'].format(compile))

def klee_execute(output_path, stdin, c_file_name, bytecode_file_path, timeout, memory, search):
        result_file = FILE_NAME['result'].format(name = c_file_name)
        result_text_path = os.path.join(output_path, result_file)
        output_dir = os.path.join(output_path, c_file_name)

        klee = KLEE['klee'].format(input = bytecode_file_path, output = output_dir, memory = memory, time = timeout, search = search,
                                    max = stdin[NUM_ARGS], num = stdin[LENGTH_ARGS], n = stdin[LENGTH_INPUT], text = result_text_path)

        os.system(CMD['bash'].format(klee))

def clean_up(path, option):
    if option == EVERTHING:
        shutil.rmtree(path)
        os.mkdir(path)

    elif option == BYTECODE_FILES:
        dir_path_list = Path(path).glob('**/*.bc')
        for file in dir_path_list:
            os.remove(str(file))


def symbolic_execution(input_path, output_path, stdin, timeout = 0, memory = 2000, search = 'random-path'):
    clean_up(output_path, EVERTHING)

    def klee_args(output_path, c_file_path):

        c_file = os.path.basename(c_file_path)
        c_file_name, _ = os.path.splitext(c_file)

        bytecode_file = FILE_NAME['bytecode'].format(name = c_file_name)
        bytecode_file_path = os.path.join(output_path, bytecode_file)

        compile(output_path, c_file_path, c_file_name, bytecode_file_path)

        klee_execute(output_path, stdin, c_file_name, bytecode_file_path, timeout, memory, search)


    if os.path.isdir(input_path):
        dir_path_list = Path(input_path).glob('**/*.c')
        for path in dir_path_list:
            c_file_path = str(path.absolute())
            klee_args(output_path, c_file_path)

    elif os.path.isfile(input_path):
        c_file_path = input_path
        klee_args(output_path, c_file_path)

    clean_up(output_path, BYTECODE_FILES)
