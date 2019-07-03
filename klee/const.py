KLEE_CMD = {
    'sym-stdin': '--sym-stdin {length}',
    'sym-args': '--sym-args 1 {max} {length}',
    'stats': 'klee-stats --print-rel-times {input}',
    'compile': 'clang -emit-llvm -c {input} -o {output}',
    'options':'{{ time klee \
                --libc=uclibc \
                --output-dir={output} \
                --only-output-states-covering-new \
                --optimize \
                --posix-runtime \
                --max-memory={memory} \
                --max-time={time} \
                --search={search} \
                {input} {sym_args} {sym_stdin};\
               }} 2> {file}',
}
