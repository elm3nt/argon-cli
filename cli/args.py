from cli.argparser import *


def se_options(args):
    return {
        'memory': args.memory,
        'search': args.search,
        'timeout': args.timeout,
    }


def credentials(args):
    return {
        'codes': args.codes,
        'passwords': args.passwords,
    }


def stdin(args):
    return {
        'num-arg': args.num_arg,
        'num-input': args.num_input,
        'length-arg': args.length_arg,
        'length-input': args.length_input,
    }


def print_help():
    parser.print_help()
    tigress_genenerate_option.print_help()
    tigress_obfuscate_option.print_help()
    se_parser.print_help()
    run_option.print_help()


