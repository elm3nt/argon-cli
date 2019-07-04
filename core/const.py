SE = 'se'
ALL = 'all'
RUN = 'run'
ONE_BYTE = 8
ANGR = 'angr'
KLEE = 'klee'
GENERATE = 'generate'
OBFUSCATE ='obfuscate'


EXT = {
    'c': '.c',
    'txt': '.txt',
    'ktest': '.ktest',
}

CMD = {
    'bash': '/bin/bash -c "{}"',
    'gcc': 'gcc {input} -o {output}',
    'run': 'echo {stdin} | {input} {arg}',
    'time': '{{ time {cmd} ; }} 2> {output}',
}

DIR_NAME = {
    'samples': 'samples',
}

FILE_NAME = {
    'c-out': '{name}.out',
    'run': '{name}_run.txt',
    'bytecode': '{name}.bc',
    'empty-c-file': 'empty.c',
    'analysis': 'analysis.csv',
    'klee-test': 'test_klee_{name}.txt',
    'angr-test': 'test_angr_{index}.txt',
}
