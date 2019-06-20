import os

from .const import *
from core.argparser import *
from tigress.main import obfuscate, generate
from ABC.main import run as angr_run

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

    elif args.option == ANGR or args.option == KLEE:
        stdin = {
            'num-arg': args.num_arg,
            'arg-length': args.length_arg,
            'num-input': args.num_input,
            'input-length': args.length_input
        }

        angr_run(input_path, output_path, stdin)
