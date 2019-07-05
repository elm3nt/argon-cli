# Argon

Argon is an automation tool to generate, obfuscate and run symbolic symbolic analysis on C source files. It uses following tools to achieve it:
* [Angr](http://angr.io/)
* [Klee](https://github.com/klee/)
* [Tigress](http://tigress.cs.arizona.edu/)


### Prerequisites

* [Docker](https://www.docker.com/)


### Set up the environment
```
$ mkdir workspace
$ cd workspace
$ mkdir out
$ git clone git@github.com:deepsadhi/argon.git
$ docker run -v $(pwd):/workspace -ti --name=argon deepsadhi/argon
$ docker start -ai argon
$ cd /workspace/argon
$ echo "export PATH=$PATH:/workspace/argon" >> ~/.bashrc  # Only if you are using Docker
```
This will mount host's workspace directory to contianer's root directory


### Generate sameple C source code with code and password authentication
Syntax
```
$ argon generate -o [output C file path] -c [code] - p [password]
```
Example
```
$ argon generate -o ../out/sample.c -c 18 -p p@ssw0rd
```

### Obfuscate generated C source code
Obfuscation options: `A` `C` `D` `V`
Syntax
```
$ argon obfuscate -i [input C file path] -o [output directory path] -nv [number of variants] -ol [obfuscation list]
```
Example
```
$ argon obfuscate -i ../out/sample.c -o ../out/obs -nv 5 -ol A AC ADC DACV
```

## Run analysis
Analysis takes single C source file or directory with C source files. The analysis report of test is saved in `analysis.csv` file of output path

### Execution time of compiled C source code
Syntax
```
$ argon run -i [input C file/dir path] -o [output directory path] -c [code] -p [password]
```
Example
```
$ argon run -i ../out/obs/AC -o ../out/out-run -c 18 -p p@ssw0rd
$ argon run -i ../out/sample.c -o ../out/out-sample -c 18 -p p@ssw0rd
```

### Run symbolic analysis using Angr, Klee
Syntax
```
$ argon (angr|klee|all) -i [input C file/dir path] -o [output directory path] -na [number of arguments] -la [length of argument] -ni [number of inputs] -li [length of input] -c [authentication code] -p [authentication password]
```
Example
```
$ argon klee -i ../out/obs/AC -o ../out/out-klee-obs -na 1 -la 2 -ni 1 -li 8 -c 18 -p p@ssw0rd
$ argon angr -i ../out/sample.c -o ../out/out-angr-sample -na 1 -la 2 -ni 1 -li 8 -c 18 -p p@ssw0rd

```
Run symbolic analysis using Agn, Klee and note execution time as well
```
$ argon all -i ../out/obs/ADC -o ../out/out-all-adc -na 1 -la 2 -ni 1 -li 8 -c 18 -p p@ssw0rd
```

## Authors

* [Deepak Adhikari](https://github.com/deepsadhi)
* [Justin Nguyen](https://github.com/Thienx99)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
