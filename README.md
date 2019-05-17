# Symbolic Analysis

Symbolic Analysis is set of scripts to automate Klee symbolic analyzer, record timing and generate stats.


### Prerequisites

* [Docker](https://www.docker.com/)


### Set up the environment

Syntax to create Docker container
```
$ docker run -v [host machine source dir]:[target machine destination dir] -ti --name=[container name] --ulimit='stack=-1:-1' [docker image name]
```
Example to create Docker container
```
$ docker run -v /home/user/workspace:/workspace -ti --name=triton --ulimit='stack=-1:-1' klee/klee
```
Keep all test C files in workspace directory of the host machine to peform the test.


## Running the tests

Start Klee container
```
$ docker start -ai klee
```

### Run tests

This script recursively traverses into test directory and looks for `C` files. For each `C` file found following tasks is performed:
1. Generate bytecode of `C` file using `LLVM`
2. Run `Klee` test on bytecode file
3. Create a directory named with`C` file in the direcotry where `C` file was found and store `Klee` output
4. Create a `time.txt` file named with `C` file in the direcotry where `C` file was found and record time taken to execute the test

Syntax
```
$ ./batch.py [test directory] "[klee symbolic input args]"
```
Example
```
$ cd /workspace/klee-analysis
$ ./batch.py tests/ "--sym-stdin 12"
```

### Generate stats

This script recursively traverses into test directory and looks for `time.txt` files. For each `time.txt` file found following information will be extracted:
1. Test file name
2. Time taken to run test on test file
3. Size of test file (in bytes)
4. Path of test file
As a last step, `analysis.csv` file is created in test directory with all stats.

Syntax
```
$ ./analysis.py [test directory]
```
Example
```
$ cd /workspace/klee-analysis
$ ./analysis.py tests/
```


## Authors

* [Deepak Adhikari](https://github.com/deepsadhi)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
