CMD = {
    'bash': '/bin/bash -c "{}"',
    'gcc': 'gcc {input} -o {output}'
}

DIR_NAME = {
    'samples': 'samples'
}

FILE_NAME = {
    'empty-c-file': 'empty.c',
    'analyis': 'analysis.csv',
}

SE = 'se'
C_EXT = '.'
ANGR = 'angr'
KLEE = 'klee'
GENERATE = 'generate'
OBFUSCATE ='obfuscate'
SYMBOLIC_EXECUTION = 'symbolic-execution'

CSV_HEAD = {
    'file-path': 'Path',
    'file-name': 'File',
    'klee-time': 'Time taken by Klee',
    'angr-time': 'Time taken by Angr',
    'file-sze': 'File size (in bytes)',
}
