import os

from .const import *
from utils import file
from shutil import copy2
from core.argparser import *
from mangr.main import run as angr_run
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
        obfuscation_combinations = {'A', 'ADC'}
        no_of_variants = args.num
        obfuscate(input_path, output_path, obfuscation_combinations, no_of_variants)

    elif args.option == ANGR or args.option == KLEE or args.option == SYMBOLIC_EXECUTION or args.option == SE:
        stdin = {
            'num-arg': args.num_arg,
            'arg-length': args.length_arg,
            'num-input': args.num_input,
            'input-length': args.length_input
        }
        symbolic_execution(input_path, output_path, stdin, args.option)


def symbolic_execution(input_path, output_path, stdin, option):
    files_path = file.list(input_path, '.c')

    for file_path in files_path:
        input_file = file.details(file_path)
        output_dir_path = os.path.join(output_path, input_file['name'])
        os.makedirs(output_dir_path, exist_ok=True)
        copy2(file_path, output_dir_path) # TODO: Remove file permissions on copy

        if option == ANGR:
            angr_run(input_path, output_dir_path, stdin)
        elif option == SYMBOLIC_EXECUTION or option == SE:
            angr_run(input_path, output_dir_path, stdin)
