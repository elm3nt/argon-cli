import os

from core.route import *
from tigress.main import obfuscate, generate
from klee.main import symbolic_execution

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

    elif args.option == 'klee':
        stdin = [args.num_args, args.length_args, args.num_input, args.length_input]
        timeout = args.timeout
        memory = args.memory
        search = args.search
        credentials = [args.password, args.code]

        symbolic_execution(input_path, output_path, stdin, timeout, memory, search, credentials)
