FROM ubuntu:18.04
LABEL Maintainer="Deepak Adhikari" Version="0.1.0-alpha"

ENV HOME='/home/argon'
ENV TOOLS='${HOME}/tools'

# Install dependencies
RUN apt-get update && apt-get install -y wget unzip python3-pip build-essential curl libcap-dev git cmake libncurses5-dev python-minimal python-pip unzip libtcmalloc-minimal4 libgoogle-perftools-dev libsqlite3-dev doxygen clang-6.0 llvm-6.0 llvm-6.0-dev llvm-6.0-tools bison flex libboost-all-dev perl zlib1g-dev minisat && apt-get clean
RUN pip3 install -U --upgrade pip
RUN pip3 install -U tabulate

# Create sym link for LLVM
RUN ln -s /usr/bin/llvm-config-6.0 /usr/bin/llvm-config && ln -s /usr/bin/clang-6.0 /usr/bin/clang && ln -s /usr/bin/clang++-6.0 /usr/bin/clang++

# Add arogn user
RUN useradd -m argon && echo argon:argon | chpasswd && echo 'argon  ALL=(root) NOPASSWD: ALL' >> /etc/sudoers
RUN mkdir -p ${TOOLS}
WORKDIR ${TOOLS}

# Z3
RUN wget https://github.com/Z3Prover/z3/archive/z3-4.8.4.zip && unzip z3-4.8.4.zip && rm z3-4.8.4.zip && cd z3-z3-4.8.4 && python scripts/mk_make.py && cd build && make && make install

# STP
RUN wget https://github.com/stp/stp/archive/2.3.3.zip && unzip 2.3.3.zip && rm 2.3.3.zip && cd stp-2.3.3 && mkdir build && cd build && cmake .. && make && make install

# ucLibc
RUN wget https://github.com/klee/klee-uclibc/archive/klee_uclibc_v1.2.zip && unzip klee_uclibc_v1.2.zip && rm klee_uclibc_v1.2.zip && cd klee-uclibc-klee_uclibc_v1.2 && ./configure --make-llvm-lib  && make -j2

# Klee build
RUN wget https://github.com/klee/klee/archive/v2.0.zip && unzip v2.0.zip && rm v2.0.zip && cd klee-2.0 && mkdir build && cd build && cmake \
-DENABLE_SOLVER_Z3=ON \
-DENABLE_SOLVER_STP=ON \
-DENABLE_UNIT_TESTS=OFF \
-DENABLE_KLEE_UCLIBC=ON \
-DENABLE_SYSTEM_TESTS=OFF \
-DENABLE_POSIX_RUNTIME=ON \
-DLLVMCC=/usr/bin/clang-6.0 \
-DLLVMCXX=/usr/bin/clang++-6.0 \
-DLLVM_CONFIG_BINARY=/usr/bin/llvm-config-6.0 \
-DKLEE_UCLIBC_PATH=../../klee-uclibc-klee_uclibc_v1.2 \
../ && make

# Angr
RUN pip3 install -U angr claripy
RUN wget https://github.com/tum-i22/obfuscation-benchmarks/raw/d11452ffb3ec7418a462f65d4034f9f1474136c8/resources/tigress-Linux-x86_64-2.2.zip && unzip tigress-Linux-x86_64-2.2.zip && rm tigress-Linux-x86_64-2.2.zip

# Add path
RUN echo 'PATH=$PATH:${TOOLS}/klee-2.0/build/bin:${TOOLS}/tigress-2.2' >> ${HOME}/.bashrc

# User and permissions
USER argon
WORKDIR ${HOME}
ADD --chown=argon:argon / ${TOOLS}
