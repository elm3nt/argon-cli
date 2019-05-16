#!/usr/bin/python3

import os
import sys
from pathlib import Path


CMD = {
    'bash': '/bin/bash -c "{}"',
    'compile': 'clang -emit-llvm -c {} -o {}',
    'test' :'{{ time klee --libc=uclibc --output-dir={} --only-output-states-covering-new --optimize --posix-runtime {} {}; }} 2> {}',
}

FILE_NAME = {
    'bytecode': '{}.bc',
    'result': '{}.time.txt'
}


def compile(test_path, c_file_path, c_file_name, bytecode_file_path):
         compile = CMD['compile'].format(c_file_path, bytecode_file_path)

         print(compile)
         os.system(CMD['bash'].format(compile))


def test(test_path, c_file_name, bytecode_file_path):
         test_result_file = FILE_NAME['result'].format(c_file_name)
         test_result_path = os.path.join(test_path, test_result_file)
         test_output_dir = os.path.join(test_path, c_file_name)
         test = CMD['test'].format(test_output_dir, bytecode_file_path, klee_args, test_result_path)
         print(test)
         os.system(CMD['bash'].format(test))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: batch [test directory] [klee symbolic input args]')
        sys.exit(1)

    test_dir = sys.argv[1]
    klee_args = sys.argv[2]

    test_dir_path_list = Path(test_dir).glob('**/*.c')
    for path in test_dir_path_list:
         c_file_path = str(path.absolute())
         c_file = os.path.basename(c_file_path)
         c_file_name, _ = os.path.splitext(c_file)
         test_path = os.path.dirname(c_file_path)
         bytecode_file = FILE_NAME['bytecode'].format(c_file_name)
         bytecode_file_path = os.path.join(test_path, bytecode_file)

         compile(test_path, c_file_path, c_file_name, bytecode_file_path)

         test(test_path, c_file_name, bytecode_file_path)

