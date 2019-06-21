import os

from .const import *
from utils import file
from shutil import copy2
from core.argparser import *
from stats.main import analysis
# from mangr.main import run as angr_run
from klee.main import run as klee_run
from tigress.main import obfuscate, generate

def run(argv):
    args = parser.parse_args()
    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)

    if args.option == 'generate':
        password = args.password
        pin = args.code
        generate(input_path, output_path, password, pin)

    elif args.option == 'obfuscate':
        obfuscation_combinations = args.obfuscation_list
        no_of_variants = args.num_variants
        obfuscate(input_path, output_path, obfuscation_combinations, no_of_variants)

    elif args.option == ANGR or args.option == KLEE or args.option == SYMBOLIC_EXECUTION or args.option == SE:
        stdin = {
            'num-arg': args.num_arg,
            'length-arg': args.length_arg,
            'num-input': args.num_input,
            'length-input': args.length_input
        }

        options = {
            'memory': args.memory,
            'search': args.search,
            'timeout': args.timeout,
        }

        symbolic_execution(input_path, output_path, stdin, args.option, options)


def symbolic_execution(input_path, output_path, stdin, tool, options):
    input_files_path = file.list(input_path, '.c')
    data = [ ['File', 'Time taken Klee', 'File size (in bytes)', 'Path'] ]

    if (os.path.isdir(output_path)):
        file.clean_up(output_path)
    else:
        os.mkdir(output_path)

    for input_file_path in input_files_path:
        input_file = file.details(input_file_path)
        input_file_size = os.path.getsize(input_file_path)
        output_dir_path = os.path.join(output_path, input_file['name'])

        os.mkdir(output_dir_path)
        copy2(input_file_path, output_dir_path) # TODO: Remove file permissions on copy

        if tool == ANGR:
            pass
            # test_results = angr_run(input_file_path, output_dir_path, stdin)
            # data.append([input_file['file'], str(test_results['time']), input_file_size, input_file_path])

        elif tool == KLEE:
            test_results = klee_run(input_file_path, output_dir_path, stdin, options)
            data.append([input_file['file'], str(test_results['time']), input_file_size, input_file_path])

        elif tool == SYMBOLIC_EXECUTION or tool == SE:
            data.append([input_file['file'], str(test_results['time']), input_file_size, input_file_path])
            pass
            # angr_run(input_path, output_dir_path, stdin)

    analysis_file_path = os.path.join(output_path, 'analysis.csv')
    analysis(analysis_file_path, data)
