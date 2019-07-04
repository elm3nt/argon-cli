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
