SE = 'se'
ONE_BYTE = 8
C_EXT = '.c'
ANGR = 'angr'
KLEE = 'klee'
GENERATE = 'generate'
OBFUSCATE ='obfuscate'
SYMBOLIC_EXECUTION = 'symbolic-execution'

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
    'angr-test': 'test_angr_{index}.txt',
}

CSV_HEAD = {
    'file-path': 'Path',
    'file-name': 'File',
    'klee-time': 'Time taken by Klee',
    'angr-time': 'Time taken by Angr',
    'file-size': 'File size (in bytes)',
}
