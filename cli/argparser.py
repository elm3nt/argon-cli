import argparse

from core.const import *


common_parser = argparse.ArgumentParser(add_help = False)
common_parser.add_argument('-o', '--output', help = 'path of file/dir to store generated file(s)')

parser = argparse.ArgumentParser(description='', usage = SUPPRESS, parents=[common_parser], prog = PROGRAM,
                                 formatter_class=RawTextHelpFormatter, epilog = 'help for each option:')
parser._optionals.title= 'Argon Help'
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)
sub_parser = parser.add_subparsers(title='argon options', dest = 'option', description='mandatory argument: \n ' +
                                  ' -o , --output         path of file/dir to store generated file(s)',
                                   metavar='usage: argon [-o] {generate,obfuscate,run,all,angr,klee}\n\n')

tigress_genenerate_option = sub_parser.add_parser(GENERATE, parents = [common_parser],
                                       help = 'generate sample C source code with code and password')
tigress_genenerate_option.add_argument('-c', '--code', type = int, default = [ None ], nargs = '*',
                                       help = 'activation code for generated program')
tigress_genenerate_option.add_argument('-p', '--password', default = [ None ], nargs = '*',
                                       help = 'password for generated program')

tigress_obfuscate_option = sub_parser.add_parser(OBFUSCATE, parents = [common_parser],
                                      help = 'obfuscate generated C source code')
tigress_obfuscate_option.add_argument('-i', '--input',
                                      help = 'path of benchmark dir/file(s)')
tigress_obfuscate_option.add_argument('-nv', '--num-variants', type = int,
                                      help = 'number of obfuscation variants to be generated')
tigress_obfuscate_option.add_argument('-ol', '--obfuscation-list', nargs = '+',
                                      help = 'obfuscation combinations list')

run_option = sub_parser.add_parser(RUN, parents = [common_parser],
                        help = 'compile c source code with different GCC optimization level')
run_option.add_argument('-ol', '--optimization-levels', choices = OPTIONS['gcc-optimization-levels'], nargs = '+',
                        help = 'gcc optimization levels (' + '|'.join(OPTIONS['gcc-optimization-levels']) +')')
run_option.add_argument('-i', '--input',
                        help = 'path of benchmark dir/file(s)')
run_option.add_argument('-c', '--codes', required = False, default = [], nargs = '+',
                        help = 'list of activaton codes seperated by comma or space')
run_option.add_argument('-p', '--passwords', required = False, default = [], nargs = '+',
                        help = 'list of passwords seperated by comma or space')

se_parser = argparse.ArgumentParser(add_help = False)
se_parser.add_argument('-i', '--input',
                       help = 'path of benchmark dir/file(s)')
se_parser.add_argument('-na', '--num-arg', type = int, default = 0,
                       help = 'number of arguments required by the program')
se_parser.add_argument('-la', '--length-arg', type = int, default = 0,
                       help = 'length of argument')
se_parser.add_argument('-ni', '--num-input', type = int, default = 0,
                       help = 'number of inputs required by the program')
se_parser.add_argument('-li', '--length-input', type = int, default = 0,
                       help = 'length of input')
se_parser.add_argument('-t', '--timeout', required = False, default = 0, type = int,
                       help = 'time to stop for symbolic analyer')
se_parser.add_argument('-c', '--codes', required = False, default = [], nargs = '+',
                       help = 'list of activaton codes seperated by comma or space')
se_parser.add_argument('-p', '--passwords', required = False, default = [], nargs = '+',
                       help = 'list of passwords seperated by comma or space')
se_parser.add_argument('-m', '--memory', required = False, default = 2000, type = int,
                       help = 'memory limit for symbolic analyzer')
se_parser.add_argument('-s', '--search', default = 'random-path', choices = OPTIONS['klee-search-algorithm'],
                       help = 'search algorithm for Klee (' + '|'.join(OPTIONS['klee-search-algorithm']) + ')')

sub_parser.add_parser(ALL, parents = [common_parser, se_parser],
                      help = 'run symbolic analysis using Angr, Klee and note execution time')
sub_parser.add_parser(ANGR, parents = [common_parser, se_parser],
                      help = 'runs symbolic analysis using Angr')
sub_parser.add_parser(KLEE, parents = [common_parser, se_parser],
                      help = 'runs symbolic analysis using Klee')



