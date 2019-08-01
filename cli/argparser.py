import argparse
from argparse import *

from core.const import *


common_parser = argparse.ArgumentParser(usage=SUPPRESS, add_help = False, prog = PROGRAM)
common_parser._optionals.title = 'mandatory argument'
common_parser.add_argument('-o', '--output', help = argparse.SUPPRESS, metavar='')

parser = argparse.ArgumentParser(description='', usage = SUPPRESS, parents=[common_parser], prog = PROGRAM,
                                 formatter_class=RawTextHelpFormatter, epilog = 'help for each option:')
parser._optionals.title= 'Argon Help'
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)
sub_parser = parser.add_subparsers(title='argon options', dest = 'option', description='mandatory argument: \n ' +
                                  ' -o , --output         path of file/dir to store generated file(s)',
                                   metavar='usage: argon {generate,obfuscate,run,all,angr,klee} [-o]\n\n')

tigress_genenerate_option = sub_parser.add_parser(GENERATE, parents = [common_parser], usage=SUPPRESS, add_help = False,
                                       formatter_class=RawTextHelpFormatter,
                                       help = 'generate sample C source code with code and password')
tigress_genenerate_option._optionals.title=' generate usage: argon generate [-o] [-c [[...]]] [-p [[...]]]'
tigress_genenerate_option.add_argument('-c', '--code', type = int, default = [ None ], nargs = '*',
                                       help = 'activation code for generated program', metavar='')
tigress_genenerate_option.add_argument('-p', '--password', default = [ None ], nargs = '*',
                                       help = 'password for generated program\n\n', metavar='')

tigress_obfuscate_option = sub_parser.add_parser(OBFUSCATE, parents = [common_parser], add_help = False, usage=SUPPRESS,
                                      formatter_class=RawTextHelpFormatter,
                                      help = 'obfuscate generated C source code')
tigress_obfuscate_option._optionals.title=' obfuscate usage: argon obfuscate [-o] [-i] [-nv] [-ol  [...]]'
tigress_obfuscate_option.add_argument('-i', '--input',
                                      help = 'path of benchmark dir/file(s)', metavar='')
tigress_obfuscate_option.add_argument('-nv', '--num-variants', type = int,
                                      help = 'number of obfuscation variants to be generated', metavar='')
tigress_obfuscate_option.add_argument('-ol', '--obfuscation-list', nargs = '+',
                                      help = 'obfuscation combinations list\n\n', metavar='')

input_parser = argparse.ArgumentParser(add_help = False, formatter_class=RawTextHelpFormatter, usage=SUPPRESS)
input_parser._optionals.title = ' symbolic execution universal arguements'
input_parser.add_argument('-i', '--input',
                        help = 'path of benchmark dir/file(s)', metavar='')
input_parser.add_argument('-c', '--codes', required = False, default = [], nargs = '+',
                        help = 'list of activaton codes seperated by comma or space', metavar='')
input_parser.add_argument('-p', '--passwords', required = False, default = [], nargs = '+',
                        help = 'list of passwords seperated by comma or space', metavar='')


run_option = sub_parser.add_parser(RUN, parents = [common_parser, input_parser], add_help = False, usage=SUPPRESS,
                        help = 'compile c source code with different GCC optimization level')
run_option._optionals.title=' run usage: argon run [-h] [-i] [-o] [-c  [...]] [-p  [...]] [-ol {' + '|'.join(OPTIONS['gcc-optimization-levels']) + '} '
run_option.add_argument('-ol', '--optimization-levels', choices = OPTIONS['gcc-optimization-levels'], nargs = '+',
                        help = 'gcc optimization levels (' + '|'.join(OPTIONS['gcc-optimization-levels']) +')', metavar='')


se_parser = argparse.ArgumentParser(add_help = False, usage=SUPPRESS)
se_parser._optionals.title = ' symbolic execution usage: argon {all,angr,klee} [-i] [-o] [-na] [-la] [-ni] [-li] [-t] [-m] [-s]'
se_parser.add_argument('-na', '--num-arg', type = int, default = 0,
                       help = 'number of arguments required by the program', metavar='')
se_parser.add_argument('-la', '--length-arg', type = int, default = 0,
                       help = 'length of argument', metavar='')
se_parser.add_argument('-ni', '--num-input', type = int, default = 0,
                       help = 'number of inputs required by the program', metavar='')
se_parser.add_argument('-li', '--length-input', type = int, default = 0,
                       help = 'length of input', metavar='')
se_parser.add_argument('-t', '--timeout', required = False, default = 0, type = int,
                       help = 'time to stop for symbolic analyer', metavar='')
se_parser.add_argument('-m', '--memory', required = False, default = 2000, type = int,
                       help = 'memory limit for symbolic analyzer', metavar='')
se_parser.add_argument('-s', '--search', default = 'random-path', choices = OPTIONS['klee-search-algorithm'],
                       help = 'search algorithm for Klee (' + '|'.join(OPTIONS['klee-search-algorithm']) + ')',
                       metavar='')

sub_parser.add_parser(ALL, parents = [common_parser, se_parser, input_parser], add_help = False,
                      help = 'run symbolic analysis using Angr, Klee and note execution time')

sub_parser.add_parser(ANGR, parents = [common_parser, se_parser, input_parser], add_help = False,
                      help = 'runs symbolic analysis using Angr')

sub_parser.add_parser(KLEE, parents = [common_parser, se_parser, input_parser], add_help = False,
                      help = 'runs symbolic analysis using Klee\n\n')
