import os

from .const import *
from utils import file
from shutil import copy2
from core.argparser import *
from stats.main import analysis
from klee.main import run as klee_run
from mangr.main import run as angr_run
from tigress.main import obfuscate, generate

def run(argv):
    args = parser.parse_args()
    option = args.option
    output_path = os.path.abspath(args.output)

    if option == GENERATE:
        code = str(args.code)
        password = args.password
        generate(output_path, password, code)

    elif (option == OBFUSCATE or option == ANGR or option == KLEE or
          option == SE or option == SYMBOLIC_EXECUTION):
        input_path = os.path.abspath(args.input)

        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        if option == OBFUSCATE:
            num_variants = args.num_variants
            obfuscation_combinations = args.obfuscation_list
            obfuscate(input_path, output_path, obfuscation_combinations, num_variants)

        elif (option == ANGR or option == KLEE or  option == SE or
              option == SYMBOLIC_EXECUTION):
            stdin = {
                'num-arg': args.num_arg,
                'length-arg': args.length_arg,
                'num-input': args.num_input,
                'length-input': args.length_input
            }

            se_options = {
                'memory': args.memory,
                'search': args.search,
                'timeout': args.timeout,
            }

            symbolic_execution(input_path, output_path, stdin, option, se_options)


def symbolic_execution(input_path, output_path, stdin, tool, options):
    input_files_path = file.list(input_path, C_EXT)
    data = [ [CSV_HEAD['file'], CSV_HEAD['time-angr'], CSV_HEAD['time-klee'],CSV_HEAD['file-size'],
              CSV_HEAD['file-path']] ]

    for input_file_path in input_files_path:
        input_file = file.details(input_file_path)
        input_file_size = os.path.getsize(input_file_path)
        output_dir_path = os.path.join(output_path, input_file['name'])

        os.mkdir(output_dir_path)
        copy2(input_file_path, output_dir_path) # TODO: Remove file permissions on copy

        if tool == ANGR:
            test_result = angr_run(input_file_path, output_dir_path, stdin)
            data.append([input_file['file'], str(test_result['time']), '', input_file_size, input_file_path])

        elif tool == KLEE:
            test_result = klee_run(input_file_path, output_dir_path, stdin, options)
            data.append([input_file['file'], '', str(test_result['time']), input_file_size, input_file_path])

        elif tool == SYMBOLIC_EXECUTION or tool == SE:
            angr_test_result = angr_run(input_file_path, output_dir_path, stdin)
            klee_test_result = klee_run(input_file_path, output_dir_path, stdin, options)
            data.append([input_file['file'], str(angr_test_result['time']), str(klee_test_result['time']),
                         input_file_size, input_file_path])

    analysis_file_path = os.path.join(output_path, FILE_NAME['analysis'])
    analysis(analysis_file_path, data)
