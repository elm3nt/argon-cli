SE = 'se'
ALL = 'all'
ONE_BYTE = 8
ANGR = 'angr'
KLEE = 'klee'
GENERATE = 'generate'
OBFUSCATE ='obfuscate'
EXECUTION = 'execution'


EXT = {
    'c': '.c',
    'txt': '.txt',
    'ktest': '.ktest',
}

CMD = {
    'bash': '/bin/bash -c "{}"',
    'gcc': 'gcc {input} -o {output}',
}

DIR_NAME = {
    'samples': 'samples',
}

FILE_NAME = {
    'c-out': '{name}.out',
    'log': '{name}_log.txt',
    'bytecode': '{name}.bc',
    'empty-c-file': 'empty.c',
    'analysis': 'analysis.csv',
    'klee-test': 'test_klee_{name}.txt',
    'angr-test': 'test_angr_{index}.txt',
}
