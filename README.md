# Argon

Argon is an automation tool to generate, obfuscate, compile and run symbolic execution on c source files. It uses following tools to achieve it:
* [Tigress](http://tigress.cs.arizona.edu/)
* [GCC](https://gcc.gnu.org/)
* [Clang](https://clang.llvm.org/)
* [Angr](http://angr.io/)
* [Klee](https://github.com/klee/)


### Prerequisites

* [Docker](https://www.docker.com/)


### Set up the environment
```
$ mkdir workspace
$ cd workspace
$ mkdir out
$ docker run -v $(pwd):/home/argon/workspace -ti --name=argon elm3nt/argon
$ cd ~/workspace
```
This will mount the host's workspace directory to the container's workspace directory situated in home directory.


### Generate c file with authentication
Generates sample c source file using `Tigress` `randomFunc`. You can provide either `activation codes` or `passwords` or both for `authentication` function.
Syntax
```
$ argon generate -o [output c file path] -c [code] - p [password]
```
**Please make sure you specify a filename in the output path with a c extension 

Example
```
$ argon generate -o out/sample.c -c 18
$ argon generate -o out/sample.c -c 18 -p p@ssw0rd
$ argon generate -o out/sample.c -c 18 -p p@ssw0rd
$ argon generate -o out/sample.c -c 18 40 -p p@ssw0rd
$ argon generate -o out/sample.c -c 18 -p p@ssw0rd secret
$ argon generate -o out/sample.c -c 18 40 -p p@ssw0rd secret
```

### Obfuscate generated c source file
Obfuscates generated c source file with `Tigress` transformations (`Abstract` `Control flow` `Data` and `Virtualization`). You can use short code of each transformations, for e.g. `A` `C` `D` `V` or any combinations of short codes such as `AC` `ADC` `DACV`.  
**Note: Make sure you use generated c source file from `generate` command. Your custom c source file might not work.**
Syntax
```
$ argon obfuscate -i [input C file path] -o [output directory path] -nv [number of variants] -ol [obfuscation list]
```
Example
```
$ argon obfuscate -i out/sample.c -o out/obs -nv 5 -ol A AC ADC DACV
```

## Execution time analysis
Generates analysis report of execution time for compiled c source file using provided `GCC` optimiazation levels (`0` `1` `2` `3` `s` `fast`). It can take input as single c source file or directory with c source files. The analysis report is saved in `analysis.csv` file of output path.

### Compile and execute c source file 
Syntax
```
$ argon run -i [input C file/dir path] -o [output directory path] -ol {0|1|2|3|s|fast} -c [code] -p [password]
```
Example
```
$ argon run -i out/obs/AC -o out/out-run -ol 0 -c 18 -p p@ssw0rd
$ argon run -i out/sample.c -o out/out-sample -ol 0 1 2 3 s fast -c 18 -p p@ssw0rd
```

### Symbolic execution analysis
Generates symbolic execution analysis report of c source files using `Klee` or `Angr` or both. The c source file must have c `args` authentication or c standard input (e.g. `scanf`) authentication or both.  It can take input as single c source file or directory with c source files. The command requires number of arguments and length of argument to perform symbolic execution, if source program has `args` based authentication. Similarly number of standard inputs and length of standard input is required for `stdin` based authentication. If source file has both `args` and `stdin` based authentication provide both of them. If you want validate whether symbolic execution tools cracked `activation codes` and `passwords` correctly, also provide codes and passwords. The analysis report with crack time,  saved in `analysis.csv` file of output path.
Syntax
```
$ argon (angr|klee|all) -i [input C file/dir path] -o [output directory path] -na [number of arguments] -la [length of argument] -ni [number of inputs] -li [length of input] -c [authentication code] -p [authentication password]
```
Example
```
$ argon klee -i out/obs/AC -o out/out-klee-obs -na 1 -la 2 -ni 1 -li 8
$ argon klee -i out/obs/AC -o out/out-klee-obs -na 1 -la 2 -ni 1 -li 8 -c 18 -p p@ssw0rd
$ argon angr -i out/sample.c -o out/out-angr-sample -na 1 -la 2 -ni 1 -li 8 -c 18 -p p@ssw0rd

```
Runs symbolic execution using Angr, Klee and notes execution time as well
```
$ argon all -i out/obs/ADC -o out/out-all-adc -na 1 -la 2 -ni 1 -li 8 -c 18 -p p@ssw0rd
```

## Authors

* [Deepak Adhikari](https://github.com/deepsadhi)
* [Justin Nguyen](https://github.com/Thienx99)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
