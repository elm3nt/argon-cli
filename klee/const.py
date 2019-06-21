EVERTHING = 1
BYTECODE_FILES = 2

NUM_ARGS = 0
LENGTH_ARGS = 1
NUM_INPUT = 2
LENGTH_INPUT =3

COMPILE = {
    'compile': 'clang -emit-llvm -c {input} -o {output}',
}

KLEE = {
    'klee' :'{{ time klee \
            --libc=uclibc \
            --output-dir={output} \
            --only-output-states-covering-new \
            --optimize \
            --posix-runtime \
            --max-memory={memory} \
            --max-time={time} \
            --search={search} \
            {input} \
            --sym-args 1 {max} {num} \
            --sym-stdin {n}; }} 2> {text}',
}

FILE_NAME = {
    'bytecode': '{name}.bc',
    'result': '{name}.time.txt'
}
