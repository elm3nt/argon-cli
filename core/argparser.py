import argparse

from core.const import *

parser = argparse.ArgumentParser(prog = 'ArgParser')
sub_parser = parser.add_subparsers(help = 'option', dest = 'option')

common_parser = argparse.ArgumentParser(add_help = False)
common_parser.add_argument('-o', '--output', help = 'input output path to store generated files')

tigress_genenerate_option = sub_parser.add_parser(GENERATE, parents = [common_parser])
tigress_genenerate_option.add_argument('-c', '--code', type = int, default = 18,
                                       help = 'input activation code for generating file')
tigress_genenerate_option.add_argument('-p', '--password', default = 'p@$$w0rd',
                                       help = 'input password for generating file')

tigress_obfuscate_option = sub_parser.add_parser(OBFUSCATE, parents = [common_parser])
tigress_obfuscate_option.add_argument('-i', '--input', help = 'enter full path to input from your current directory!')
tigress_obfuscate_option.add_argument('-nv', '--num-variants', type = int,
                                      help = 'the number of variants to be created')
tigress_obfuscate_option.add_argument('-ol', '--obfuscation-list', nargs = '*',
                                      help = 'enter list of obfuscation combinations')

se_parser = argparse.ArgumentParser(add_help = False)
se_parser.add_argument('-i', '--input', help = 'enter full path to input from your current directory!')
se_parser.add_argument('-na', '--num-arg', type = int, default = 0, help = 'enter number of arguments for the program')
se_parser.add_argument('-la', '--length-arg', type = int, default = 0,
                       help = 'enter length of arguments for the program')
se_parser.add_argument('-ni', '--num-input', type = int, default = 0, help = 'enter number of inputs for the program')
se_parser.add_argument('-li', '--length-input', type = int, default = 0,
                       help = 'enter length of inputs for the program')
se_parser.add_argument('-t', '--timeout', required = False, default = 0, type = int,
                       help = 'enter time to stop symbolic analyzer')
se_parser.add_argument('-c', '--codes', required = False, default = [], nargs = '*',
                       help = 'enter list of activaton codes')
se_parser.add_argument('-p', '--passwords', required = False, default = [],
                       nargs = '*', help = 'enter list of passwords')
se_parser.add_argument('-m', '--memory', required = False, default = 2000, type = int,
                       help = 'enter memory limit for symbolic analyzer')
se_parser.add_argument('-s', '--search', default = 'random-path',
                       choices = ['dfs', 'random-state', 'random-path', 'nurs:covnew', 'nurs:md2u', 'nurs:depth',
                                  'nurs:icnt', 'nurs:cpicnt', 'nurs:qc'],
                       help = 'select search type to perform symbolic analysis')

sub_parser.add_parser(ALL, parents = [common_parser, se_parser])
sub_parser.add_parser(RUN, parents = [common_parser, se_parser])
sub_parser.add_parser(ANGR, parents = [common_parser, se_parser])
sub_parser.add_parser(KLEE, parents = [common_parser, se_parser])
