import argparse

from core.const import *


common_parser = argparse.ArgumentParser(add_help = False)
common_parser.add_argument('-o', '--output', help = 'Path of file/dir to store generated file(s)')

parser = argparse.ArgumentParser(prog = 'Argon', parents = [common_parser], add_help = False)
sub_parser = parser.add_subparsers(dest = 'option')

tigress_genenerate_option = sub_parser.add_parser(GENERATE, parents = [common_parser], help = 'generate sample C source code with code and password')
tigress_genenerate_option.add_argument('-c', '--code', type = int, default = None, nargs = '+', #const = 18,
                                       help = 'activation code for generated program')
tigress_genenerate_option.add_argument('-p', '--password', default = None, nargs = '+', #const = 'p@ssword',
                                       help = 'password for generated program')

tigress_obfuscate_option = sub_parser.add_parser(OBFUSCATE, parents = [common_parser], help = 'obfuscate generated C source code')
tigress_obfuscate_option.add_argument('-i', '--input',
                                      help = 'path of benchmark dir/file(s)')
tigress_obfuscate_option.add_argument('-nv', '--num-variants', type = int,
                                      help = 'number of obfuscation variants to be generated')
tigress_obfuscate_option.add_argument('-ol', '--obfuscation-list', nargs = '+',
                                      help = 'obfuscation combinations list')

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
se_parser.add_argument('-s', '--search', default = 'random-path',
                       choices = ['dfs', 'random-state', 'random-path', 'nurs:covnew', 'nurs:md2u', 'nurs:depth',
                                  'nurs:icnt', 'nurs:cpicnt', 'nurs:qc'],
                       help = 'search algorithm for Klee ' +
                              '(dfs|random-state|random-path|nurs:covnew|nurs:md2u|nurs:depth|nurs:icnt|nurs:cpicnt|nurs:qc')

sub_parser.add_parser(ALL, parents = [common_parser, se_parser], help = 'run symbolic analysis using Angr, Klee and note execution time')
sub_parser.add_parser(RUN, parents = [common_parser, se_parser], help = 'notes execution time written to analysis.csv')
sub_parser.add_parser(ANGR, parents = [common_parser, se_parser], help = 'runs symbolic analysis using Angr')
sub_parser.add_parser(KLEE, parents = [common_parser, se_parser], help = 'runs symbolic analysis using Klee')


