import argparse

parser = argparse.ArgumentParser(prog = 'ArgParser')
sub_parser = parser.add_subparsers(help = 'option', dest = 'option')

common_parser = argparse.ArgumentParser(add_help = False)
common_parser.add_argument('-i', '--input', help = 'enter full path to input from your current directory!')
common_parser.add_argument('-o', '--output', help = 'input output path to store generated files')

tigress_genenerate_option = sub_parser.add_parser('generate', parents = [common_parser])
tigress_genenerate_option.add_argument('-p', '--password', help = 'input password for generating file')
tigress_genenerate_option.add_argument('-c', '--code', help = 'input activation code for generating file')
tigress_obfuscate_option = sub_parser.add_parser('obfuscate', parents = [common_parser])
tigress_obfuscate_option.add_argument('n', type=int, help = 'the number of variants to be created')

se_parser = argparse.ArgumentParser(add_help = False)
se_parser.add_argument('-na', '--num-arg', type = int, help = 'enter number of arguments for the program')
se_parser.add_argument('-la', '--length-arg', type = int, help = 'enter length of arguments for the program')
se_parser.add_argument('-ni', '--num-input', type = int, help = 'enter number of inputs for the program')
se_parser.add_argument('-li', '--length-input', type = int, help = 'enter length of inputs for the program')
se_parser.add_argument('-t', '--timeout', type = int, help = 'enter time to stop symbolic analyzer')
se_parser.add_argument('-c', '--code', type = list, help = 'enter list of activaton codes')
se_parser.add_argument('-p', '--password', type = list, help = 'enter list of passwords')

angr_option = sub_parser.add_parser('angr', parents = [common_parser, se_parser])

klee_option = sub_parser.add_parser('klee', parents = [common_parser, se_parser])
klee_option.add_argument('-m', '--memory', type = int, help = 'enter memory limit for symbolic analyzer')
klee_option.add_argument('-s', '--search', help = 'select search type to perform symbolic analysis')
