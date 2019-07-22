import os
import sys

from .const import *
from utils import fs
from core.args import *
from core.argparser import *
from .se import run as run_se
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
        fs.mkdir(output_path)
        run_code(input_path, output_path, args.optimization_levels, credentials(args))

    elif (tool == ANGR or tool == KLEE or tool == ALL):
        input_path = os.path.abspath(args.input)
        fs.mkdir(output_path)
        run_se(input_path, output_path, stdin(args), tool, se_options(args), credentials(args))


