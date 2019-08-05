'''Cli module.'''
import os
import re
import sys

from utils import fs
from cli.argparser import PARSER
from se.main import run as run_se
from core.main import file_iterator
from code.main import run as run_code
from tigress.main import obfuscate, generate
from cli.args import print_help, credentials, stdin, se_options
from core.const import RE_OBFUSCATION, RUN, KLEE, ALL, ANGR, GENERATE, OBFUSCATE


def run(argv):
    '''
    Selects which tool to be used by user.

    Arguments:
        argv {list} -- List of arguements
    '''
    if len(argv) <= 1:
        print_help()
        sys.exit(1)

    try:
        args = PARSER.parse_args()
    except BaseException:
        sys.exit(1)

    tool = args.option
    output_path = os.path.abspath(args.output)

    if tool == GENERATE:
        codes = args.codes
        passwords = args.passwords
        generate(output_path, codes, passwords)

    elif tool == OBFUSCATE:
        num_variants = args.num_variants
        input_path = os.path.abspath(args.input)
        fs.mkdir(output_path)
        obfuscation_combinations = args.obfuscation_list

        for obs in obfuscation_combinations:
            if not re.search(RE_OBFUSCATION, obs):
                print(
                    'One more more items in the list does not contain [A, C, D, V]')
                print('Error at: ' + obs)
                sys.exit(1)

        obfuscate(
            input_path,
            output_path,
            obfuscation_combinations,
            num_variants)

    elif tool == RUN:
        input_path = os.path.abspath(args.input)
        fn_args = {
            'credentials': credentials(args),
            'levels': args.optimization_levels,
        }
        file_iterator(input_path, output_path, RUN, run_code, fn_args)

    elif (tool == ANGR or tool == KLEE or tool == ALL):
        input_path = os.path.abspath(args.input)
        fn_args = {
            'tool': tool,
            'stdin': stdin(args),
            'options': se_options(args),
            'credentials': credentials(args),
        }
        file_iterator(input_path, output_path, tool, run_se, fn_args)
