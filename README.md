<h1 align="center">Argon</h1>
<p align="center">
  An automation tool to generate, obfuscate, compile and run symbolic execution on c source files
</p>

![Argon Architecture](architecture.png)


## Features

- Generates sample c source code using [Tigress](http://tigress.cs.arizona.edu/). The program requires activation codes and passwords to run 
- Compiles c source files with different optimization levels using [GCC](https://gcc.gnu.org/) and run it
- Compiles c source files to bytecodes using [Clang](https://clang.llvm.org/)
- Runs symbolic execution using [Angr](http://angr.io/) and [Klee](https://github.com/klee/)
- Generates analysis report of symbolic execution


## Quick start

Install [Docker](https://www.docker.com/) and follow the commands

```
$ mkdir workspace
$ cd workspace
$ mkdir out
$ docker run -v $(pwd):/home/argon/workspace -ti --name=argon elm3nt/argon
$ cd ~/workspace
```
This mmounts workspace directory created in host machine to the container home directory. This helps to easly access benchmark and test results files.


## Generate c source file with authentication function

Generates sample c source file using Tigress randomFunc option. You can provide either activation codes or passwords or both for authentication function.

Syntax
```
$ argon generate -o [output c file path] -c [code] - p [password]
```

**Note: Please make sure you specify filename with a extension in output path.**


Example
```
$ argon generate -o out/code.c -c 18
$ argon generate -o out/password.c -p secret
$ argon generate -o out/codepass.c -c 18 -p secret
```

## Obfuscate generated c source file

Obfuscates generated c source file with Tigress transformations (Abstract, Control flow, Data and Virtualization). Use short code of each transformations, for e.g. A, C, D V or any combinations of short codes such as AC, ADC, DACV.  

**Note: Make sure you use generated c source file from `generate` command. Your custom c source file might not work.**

Syntax
```
$ argon obfuscate -i [input C file path] -o [output directory path] -nv [number of variants] -ol [obfuscation list]
```

Example
```
$ argon obfuscate -i out/codepass.c -o out/obs -nv 5 -ol A AC ADC DACV
```

## Execution time analysis

It takes input as c source file(s). You can provide single c source file path. If you provide directory path it will recursively search for c source files in that direcotry. Then these c source files are compiled using GCC with provied optimiazation levels (0, 1, 2, 3, s, fast) in the options. The analysis report is saved in analysis.csv file of output path.

Syntax to compile and execute c source file 

```
$ argon run -i [input C file/dir path] -o [output directory path] -ol {0|1|2|3|s|fast} -c [code] -p [password]
```

Example
```
$ argon run -i out/obs/codepass/AC -o out/out-run -ol 0 -c 18 -p secret
$ argon run -i out/sample.c -o out/out-sample -ol 0 1 2 3 s fast -c 18 -p secret
```

Analysis report

|File|File size (in bytes)|GCC optimization level|Time taken to run (in secs)|Path|
|----|--------------------|----------------------|---------------------------|----|
|sample_o0.out|12824|0|0.001|/home/argon/workspace/out/out-sample/sample/sample_o0.out|
|sample_o1.out|8680|1|0.001|/home/argon/workspace/out/out-sample/sample/sample_o1.out|
|sample_o2.out|8680|2|0.001|/home/argon/workspace/out/out-sample/sample/sample_o2.out|
|sample_o3.out|8680|3|0.003|/home/argon/workspace/out/out-sample/sample/sample_o3.out|
|sample_os.out|8728|s|0.001|/home/argon/workspace/out/out-sample/sample/sample_os.out|
|sample_ofast.out|10160|fast|0.001|/home/argon/workspace/out/out-sample/sample/sample_ofast.out|


## Symbolic execution analysis

Generates symbolic execution analysis report of c source files using `Klee` or `Angr` or both. It takes input as c source file(s). You can provide single c source file path. Or if you provide directory path it will recursively search for c source files in that direcotry. The analysis report with crack time,  saved in `analysis.csv` file of output path.
- The c source file must have either c `args` authentication or c standard stdin (e.g. `scanf`) authentication or both
- If source program has c `args` based authentication, the command requires number of arguments and length of argument to perform symbolic execution
- Similarly if source program has c `stdin` based authentication number of standard inputs and length of standard input is required
- If source file has both `args` and `stdin` based authentication provide both of them
- If you want validate whether symbolic execution tools cracked activation codes and passwords correctly, provide activation codes and passwords in the command

Syntax
```
$ argon (angr|klee|all) -i [input C file/dir path] -o [output directory path] -na [number of arguments] -la [length of argument] -ni [number of inputs] -li [length of input] -c [authentication codes] -p [authentication passwords]
```

Example
```
$ argon angr -i out/code.c -o out/out-angr-code -na 1 -la 2 -c 18 # Does not verify code after running symbolic execution
$ argon klee -i out/obs/codepass/AC -o out/out-klee-obs -na 1 -la 2 -ni 1 -li 6 # Varifies activation codes and password after running symbolic execution
```

Run symbolic execution using Angr, Klee and notes execution time as well
```
$ argon all -i out/obs/codepass/ADC -o out/out-all-adc -na 1 -la 2 -ni 1 -li 8 -c 18 -p secret
```

Sample anlysis report


## Authors

* [Deepak Adhikari](https://github.com/deepsadhi)
* [Justin Nguyen](https://github.com/Thienx99)


## License

This source code is released under the [MIT License](LICENSE.md)
