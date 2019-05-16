#!/usr/bin/python3

import os
import sys
from pathlib import Path


if len(sys.argv) < 2:
    print('Usage: batch [test directory]')
    sys.exit(1)

root_dir = sys.argv[1]


SYM_STDIN = "--sym-stdin 12"
pathlist = Path(root_dir).glob('**/*.c')
BASH = '/bin/bash -c "{}"'
for path in pathlist:
     c_file_path = str(path.absolute())
     c_file = os.path.basename(c_file_path)
     c_file_name, _ = os.path.splitext(c_file)
     test_directory_path = os.path.dirname(c_file_path)
     bytecode_file = '{}.bc'.format(c_file_name)
     bytecode_file_path = os.path.join(test_directory_path, bytecode_file)
     compile = 'clang -emit-llvm -c {} -o {}'.format(c_file_path, bytecode_file_path)
     print(compile)
     os.system(BASH.format(compile))
     
     test_result_file = '{}.time.txt'.format(c_file_name)
     test_result_path = os.path.join(test_directory_path, test_result_file)
     test_output_dir = os.path.join(test_directory_path, c_file_name)
     test =  '{{ time klee --libc=uclibc --output-dir={} --only-output-states-covering-new --optimize --posix-runtime {} {}; }} 2> {}'.format(test_output_dir, bytecode_file_path, SYM_STDIN, test_result_path)
     print(test)
     os.system(BASH.format(test))
    
# os.system('/bin/bash -c "{ time klee --libc=uclibc --only-output-states-covering-new --optimize --posix-runtime ./tests/install.bc --sym-stdin 12; } 2> result.txt "')


