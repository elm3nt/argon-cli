import os
import sys

from .args import *
from utils import fs
from core.const import *
from .argparser import *
from se.main import run as run_se
from core.main import file_iterator
from code.main import run as run_code
from tigress.main import obfuscate, generate


def run(argv):
    if len(sys.argv) <= 2:
        print_help()
        sys.exit(1)

    try:
        args = parser.parse_args()
    except:
        sys.exit(1)

    tool = args.option
    output_path = os.path.abspath(args.output)

    if tool == GENERATE:
        code = str(args.code)
        password = str(args.password)
        generate(output_path, code, password)

    elif tool == OBFUSCATE:
        num_variants = args.num_variants
        input_path = os.path.abspath(args.input)
        fs.mkdir(output_path)
        obfuscation_combinations = args.obfuscation_list
        obfuscate(input_path, output_path, obfuscation_combinations, num_variants)

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
