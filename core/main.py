import os
import sys

from .const import *
from utils import file
from core.args import *
from core.argparser import *
from core.tool import run as run_tool
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
        code = args.code
        password = args.password
        count = 0

        if len(code) or len(password) > 1:
            count = len(code)

        generate(output_path, code, password, count)

    elif tool == OBFUSCATE:
        num_variants = args.num_variants
        input_path = os.path.abspath(args.input)
        file.make_dir_if_not_exists(output_path)
        obfuscation_combinations = args.obfuscation_list
        obfuscate(input_path, output_path, obfuscation_combinations, num_variants, tool)

    elif (tool == RUN or tool == ANGR or tool == KLEE or tool == ALL):
        input_path = os.path.abspath(args.input)
        file.make_dir_if_not_exists(output_path)
        run_tool(input_path, output_path, stdin(args), tool, se_options(args), credentials(args))


