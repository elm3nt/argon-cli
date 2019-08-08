```
Argon commands:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

mandatory argument: ALL TOOLS REQUIRE THIS ARGUEMENT!!
   -o , --output         path of file/dir to store generated file(s)

argon tool options:

  usage: argon {run,all,angr,klee,generate,obfuscate} [-o]

    generate            generate sample c source code with code and password
    obfuscate           obfuscate generated c source code
    run                 compile c source code with different GCC optimization level
    all                 run symbolic analysis using Angr, Klee and note execution time
    angr                runs symbolic analysis using Angr
    klee                runs symbolic analysis using Klee
                        
help for each option:

 generate usage: argon generate [-o] [-c [[...]]] [-p [[...]]]:
 
  -c, --codes           activation code for generated program
  -p, --passwords       password for generated program
                        
 obfuscate usage: argon obfuscate [-i] [-o] [-nv] [-ol  [...]]:
 
  -i, --input          path of benchmark dir/file(s)
  -nv, --num-variants  number of obfuscation variants to be generated
  -ol, --obfuscation-list
                       obfuscation combinations list
 
 symbolic execution and run universal arguements: 
  -i, --input          path of benchmark dir/file(s)
  -c, --codes          list of activaton codes seperated by comma or space
  -p, --passwords      list of passwords seperated by comma or space
 
 symbolic execution usage: argon {all,angr,klee} [-i] [-o] [-na] [-la] [-ni] [-li] [-t] [-m] [-s]:
 
  -na , --num-arg       number of arguments required by the program
  -la , --length-arg    length of argument
  -ni , --num-input     number of inputs required by the program
  -li , --length-input  length of input
  -t , --timeout        time to stop for symbolic analyer
  -m , --memory         memory limit for symbolic analyzer
  -s , --search         search algorithm for Klee (dfs|random-state|random-pat
                        h|nurs:covnew|nurs:md2u|nurs:depth|nurs:icnt|nurs:cpic
                        nt|nurs:qc)
                        
 run usage: argon run [-i] [-o] [-c  [...]]  [-p  [...]] [-ol {0|1|2|3|s|fast}:
 
  -ol, --optimization-levels
                        gcc optimization levels (0|1|2|3|s|fast)
```
