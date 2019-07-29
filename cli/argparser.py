import argparse
from argparse import *

from core.const import *

common_parser = argparse.ArgumentParser(usage=SUPPRESS, prog = PROGRAM, add_help = False, formatter_class=RawTextHelpFormatter)
common_parser._optionals.title = "mandatory argument"
common_parser.add_argument('-o', '--output', help = 'path of file/dir to store generated file(s)', metavar='')

parser = argparse.ArgumentParser(description="", usage=SUPPRESS, prog = PROGRAM, parents = [common_parser], add_help = False, formatter_class=RawTextHelpFormatter)
sub_parser = parser.add_subparsers(title='argon options', metavar='usage: argon [-o] {generate,obfuscate,run,all,angr,klee}')

tigress_genenerate_option = sub_parser.add_parser(GENERATE, parents = [common_parser], formatter_class=RawTextHelpFormatter,
                                       help = 'generate sample C source code with code and password\n')
tigress_genenerate_option.add_argument('-c', '--code', type = int, default = [ None ], nargs = '*',
                                       help = 'activation code for generated program', metavar='')
tigress_genenerate_option.add_argument('-p', '--password', default = [ None ], nargs = '*',
                                       help = 'password for generated program', metavar='')

tigress_obfuscate_option = sub_parser.add_parser(OBFUSCATE, parents = [common_parser],
                                      help = 'obfuscate generated C source code')
tigress_obfuscate_option.add_argument('-i', '--input',
                                      help = 'path of benchmark dir/file(s)', metavar='')
tigress_obfuscate_option.add_argument('-nv', '--num-variants', type = int,
                                      help = 'number of obfuscation variants to be generated', metavar='')
tigress_obfuscate_option.add_argument('-ol', '--obfuscation-list', nargs = '+',
                                      help = 'obfuscation combinations list', metavar='')

input_parser = argparse.ArgumentParser(add_help = False)
input_parser.add_argument('-i', '--input',
                        help = 'path of benchmark dir/file(s)', metavar='')
input_parser.add_argument('-c', '--codes', required = False, default = [], nargs = '+',
                        help = 'list of activaton codes seperated by comma or space', metavar='')
input_parser.add_argument('-p', '--passwords', required = False, default = [], nargs = '+',
                        help = 'list of passwords seperated by comma or space', metavar='')


run_option = sub_parser.add_parser(RUN, parents = [common_parser, input_parser],
                        help = 'compile c source code with different GCC optimization level')
run_option.add_argument('-ol', '--optimization-levels', choices = OPTIONS['gcc-optimization-levels'], nargs = '+',
                        help = 'gcc optimization levels (' + '|'.join(OPTIONS['gcc-optimization-levels']) +')', metavar='')

se_parser = argparse.ArgumentParser(add_help = False)
se_parser._optionals.title = 'Symbolic Execution'
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

sub_parser.add_parser(ALL, parents = [common_parser, se_parser, input_parser],
                      help = 'run symbolic analysis using Angr, Klee and note execution time')
sub_parser.add_parser(ANGR, parents = [common_parser, se_parser, input_parser],
                      help = 'runs symbolic analysis using Angr')
sub_parser.add_parser(KLEE, parents = [common_parser, se_parser, input_parser],
                      help = 'runs symbolic analysis using Klee\n')


