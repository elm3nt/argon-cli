'''Module to simplify arguements.'''
from cli.argparser import PARSER, TIGRESS_GENERATE, TIGRESS_OBFUSCATE, \
                          RUN_OPTION, SE_PARSER


def se_options(args):
    '''
    Symbolic execution optional options.

    Arguments:
        args {list} -- List of arguments

    Returns:
        list -- Symbolic execution optional arguments chosen by user
    '''
    return {
        'memory': args.memory,
        'search': args.search,
        'timeout': args.timeout,
    }


def credentials(args):
    '''
    Credentials for password and activation code. Used to check whether the
    symbolic execution tools found the password and/or activation code.

    Arguments:
        args {list} -- List of arguments
    Returns:
        list -- Credentials arguements chosen by user
    '''
    return {
        'codes': args.codes,
        'passwords': args.passwords,
    }


def stdin(args):
    '''
    Symbolic execution main arguements for the tools, KLEE and ANGR, to function.

    Arguments:
        args {list} -- List of arguements

    Returns:
        list -- Input arguements for the number and length of input and/or arg
    '''
    return {
        'num-arg': args.num_arg,
        'num-input': args.num_input,
        'length-arg': args.length_arg,
        'length-input': args.length_input,
    }


def print_help():
    '''
    Prints help for each of features of Argon.
    '''
    PARSER.print_help()
    TIGRESS_GENERATE.print_help()
    TIGRESS_OBFUSCATE.print_help()
    SE_PARSER.print_help()
    RUN_OPTION.print_help()
