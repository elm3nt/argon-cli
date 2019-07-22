SE = 'se'
ALL = 'all'
RUN = 'run'
ONE_BYTE = 8
ANGR = 'angr'
KLEE = 'klee'
PROGRAM = 'argon'
GENERATE = 'generate'
OBFUSCATE ='obfuscate'


EXT = {
    'c': '.c',
    'txt': '.txt',
    'ktest': '.ktest',
}

CMD = {
    'bash': '/bin/bash -c "{}"',
    'time': '{{ time {cmd} ; }} 2> {output}',
    'gcc': 'gcc -O{level} {input} -o {output}',
    'run': 'printf "{stdin}" | {input} {args}',
}

DIR_NAME = {
    'samples': 'samples',
}

OPTIONS = {
    'gcc-optimization-levels': ['0', '1', '2', '3', 's', 'fast'],
    'klee-search-algorithm': ['dfs', 'random-state', 'random-path', 'nurs:covnew', 'nurs:md2u', 'nurs:depth',
                              'nurs:icnt', 'nurs:cpicnt', 'nurs:qc'],
}

FILE_NAME = {
    'run': '{name}_run.txt',
    'bytecode': '{name}.bc',
    'empty-c-file': 'empty.c',
    'analysis': 'analysis.csv',
    'c-out': '{name}_o{level}.out',
    'klee-test': 'test_klee_{name}.txt',
    'angr-test': 'test_angr_{index}.txt',
}
