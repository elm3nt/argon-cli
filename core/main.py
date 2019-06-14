import os
import argparse
import getopt

from tigress.main import obfuscate, generate

def run(argv):
    parent_parser = argparse.ArgumentParser(add_help = False)
    parent_parser.add_argument('-i', '--input', help = 'type full path to input from your current directory!')
    parent_parser.add_argument('-o', '--out', help = 'input output path to store generated files')

    parser = argparse.ArgumentParser(prog = 'Tigress')
    subparser = parser.add_subparsers(help = 'option', dest = 'option')

    gen_parser = subparser.add_parser('generate', parents = [parent_parser])
    gen_parser.add_argument('-pa', '--password', help = 'input password for generating file')
    gen_parser.add_argument('-a', '--code', help = 'input activation code for generating file')

    obs_parser = subparser.add_parser('obfuscate', parents = [parent_parser])
    obs_parser.add_argument('num', type=int, help = 'the number of variants to be created')

    args = parser.parse_args()

    if args.option == 'generate':
        input_path = os.path.abspath(args.input)
        output_path = os.path.abspath(args.out)
        password = args.password
        pin = args.code

        generate(input_path, output_path, password, pin)

    elif args.option == 'obfuscate':
        obfuscation_combinations = {'A', 'ADC'}
        input_path = os.path.abspath(args.input)
        output_path = os.path.abspath(args.out)
        no_of_variants = args.num

        print(input_path)
        obfuscate(input_path, output_path, obfuscation_combinations, no_of_variants)
