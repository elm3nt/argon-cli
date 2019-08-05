'''Argument module.'''
import argparse
from argparse import SUPPRESS, RawTextHelpFormatter

from core.const import PROGRAM, GENERATE, OBFUSCATE, RUN, KLEE, ANGR, ALL, \
                       VERSION, OPTIONS

COMMON_PARSER = argparse.ArgumentParser(
    usage=SUPPRESS, add_help=False, prog=PROGRAM)
COMMON_PARSER._optionals.title = 'mandatory argument'
COMMON_PARSER.add_argument(
    '-o',
    '--output',
    help=argparse.SUPPRESS,
    metavar='')

PARSER = argparse.ArgumentParser(
    description='',
    usage=SUPPRESS,
    parents=[COMMON_PARSER],
    prog=PROGRAM,
    formatter_class=RawTextHelpFormatter,
    epilog='help for each option:')
PARSER._optionals.title = 'Argon Help'
PARSER.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s ' +
    VERSION)
SUB_PARSER = PARSER.add_subparsers(
    title='argon options',
    dest='option',
    description='mandatory argument: \n ' \
    ' -o , --output         path of file/dir to store generated file(s)',
    metavar='usage: argon {generate,obfuscate,run,all,angr,klee} [-o]\n\n')

TIGRESS_GENERATE = SUB_PARSER.add_parser(
    GENERATE,
    parents=[COMMON_PARSER],
    usage=SUPPRESS,
    add_help=False,
    formatter_class=RawTextHelpFormatter,
    help='generate sample C source code with code and password')
TIGRESS_GENERATE._optionals.title = ' generate usage: argon generate [-o] ' \
    '[-c [[...]]] [-p [[...]]]'
TIGRESS_GENERATE.add_argument(
    '-c',
    '--codes',
    type=int,
    default=[None],
    nargs='*',
    help='activation code for generated program',
    metavar='')
TIGRESS_GENERATE.add_argument(
    '-p',
    '--passwords',
    default=[None],
    nargs='*',
    help='password for generated program\n\n',
    metavar='')

TIGRESS_OBFUSCATE = SUB_PARSER.add_parser(
    OBFUSCATE,
    parents=[COMMON_PARSER],
    add_help=False,
    usage=SUPPRESS,
    formatter_class=RawTextHelpFormatter,
    help='obfuscate generated C source code')
TIGRESS_OBFUSCATE._optionals.title = ' obfuscate usage: argon obfuscate [-o] ' \
    '[-i] [-nv] [-ol  [...]]'
TIGRESS_OBFUSCATE.add_argument(
    '-i',
    '--input',
    help='path of benchmark dir/file(s)',
    metavar='')
TIGRESS_OBFUSCATE.add_argument(
    '-nv',
    '--num-variants',
    type=int,
    help='number of obfuscation variants to be generated',
    metavar='')
TIGRESS_OBFUSCATE.add_argument(
    '-ol',
    '--obfuscation-list',
    nargs='+',
    help='obfuscation combinations list\n\n',
    metavar='')

INPUT_PARSER = argparse.ArgumentParser(
    add_help=False,
    formatter_class=RawTextHelpFormatter,
    usage=SUPPRESS)
INPUT_PARSER._optionals.title = ' symbolic execution universal arguements'
INPUT_PARSER.add_argument('-i', '--input',
                          help='path of benchmark dir/file(s)', metavar='')
INPUT_PARSER.add_argument(
    '-c',
    '--codes',
    required=False,
    default=[],
    nargs='+',
    help='list of activaton codes seperated by comma or space',
    metavar='')
INPUT_PARSER.add_argument(
    '-p',
    '--passwords',
    required=False,
    default=[],
    nargs='+',
    help='list of passwords seperated by comma or space',
    metavar='')


RUN_OPTION = SUB_PARSER.add_parser(
    RUN,
    parents=[
        COMMON_PARSER,
        INPUT_PARSER],
    add_help=False,
    usage=SUPPRESS,
    help='compile c source code with different GCC optimization level')
RUN_OPTION._optionals.title = ' run usage: argon run [-h] [-i] [-o] ' \
    '[-c  [...]]  [-p  [...]] [-ol {' + '|'.join(
        OPTIONS['gcc-optimization-levels']) + '} '
RUN_OPTION.add_argument(
    '-ol',
    '--optimization-levels',
    choices=OPTIONS['gcc-optimization-levels'],
    nargs='+',
    help='gcc optimization levels (' +
    '|'.join(
        OPTIONS['gcc-optimization-levels']) +
    ')',
    metavar='')


SE_PARSER = argparse.ArgumentParser(add_help=False, usage=SUPPRESS)
SE_PARSER._optionals.title = ' symbolic execution usage: argon ' \
    '{all,angr,klee} [-i] [-o] [-na] [-la] [-ni] [-li] [-t] [-m] [-s]'
SE_PARSER.add_argument(
    '-na',
    '--num-arg',
    type=int,
    default=0,
    help='number of arguments required by the program',
    metavar='')
SE_PARSER.add_argument('-la', '--length-arg', type=int, default=0,
                       help='length of argument', metavar='')
SE_PARSER.add_argument(
    '-ni',
    '--num-input',
    type=int,
    default=0,
    help='number of inputs required by the program',
    metavar='')
SE_PARSER.add_argument('-li', '--length-input', type=int, default=0,
                       help='length of input', metavar='')
SE_PARSER.add_argument('-t', '--timeout', required=False, default=0, type=int,
                       help='time to stop for symbolic analyer', metavar='')
SE_PARSER.add_argument(
    '-m',
    '--memory',
    required=False,
    default=2000,
    type=int,
    help='memory limit for symbolic analyzer',
    metavar='')
SE_PARSER.add_argument(
    '-s',
    '--search',
    default='random-path',
    choices=OPTIONS['klee-search-algorithm'],
    help='search algorithm for Klee (' +
    '|'.join(
        OPTIONS['klee-search-algorithm']) +
    ')',
    metavar='')

SUB_PARSER.add_parser(
    ALL,
    parents=[
        COMMON_PARSER,
        SE_PARSER,
        INPUT_PARSER],
    add_help=False,
    help='run symbolic analysis using Angr, Klee and note execution time')

SUB_PARSER.add_parser(
    ANGR,
    parents=[
        COMMON_PARSER,
        SE_PARSER,
        INPUT_PARSER],
    add_help=False,
    help='runs symbolic analysis using Angr')

SUB_PARSER.add_parser(
    KLEE,
    parents=[
        COMMON_PARSER,
        SE_PARSER,
        INPUT_PARSER],
    add_help=False,
    help='runs symbolic analysis using Klee\n\n')
