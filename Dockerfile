FROM ubuntu:18.04
LABEL Maintainer="Deepak Adhikari"

# Install Klee dependencies
RUN apt-get update && apt-get install -y wget unzip python3-pip curl \
  build-essential libcap-dev git cmake libncurses5-dev python-minimal \
  python-pip libtcmalloc-minimal4 libgoogle-perftools-dev libsqlite3-dev \
  doxygen clang-6.0 llvm-6.0 llvm-6.0-dev llvm-6.0-tools bison flex sudo \
  libboost-all-dev perl zlib1g-dev minisat vim gcc-4.8 g++-4.8 && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

# Install dependencies for klee-stats
RUN pip3 install -U --upgrade pip
RUN pip2 install -U tabulate==0.8.3

# Create sym link for LLVM
RUN ln -s /usr/bin/llvm-config-6.0 /usr/bin/llvm-config && \
  ln -s /usr/bin/clang-6.0 /usr/bin/clang && \
  ln -s /usr/bin/clang++-6.0 /usr/bin/clang++

# Add arogn user
RUN useradd -m argon && echo argon:argon | chpasswd && \
  echo 'argon  ALL=(root) NOPASSWD: ALL' >> /etc/sudoers
RUN mkdir -p /home/argon/tools
WORKDIR /home/argon/tools

# Build and install Z3
RUN wget https://github.com/Z3Prover/z3/archive/z3-4.8.4.zip && \
  unzip z3-4.8.4.zip && rm z3-4.8.4.zip && cd z3-z3-4.8.4 && \
  python scripts/mk_make.py && cd build && make && make install

# Build and install STP
RUN wget https://github.com/stp/stp/archive/2.3.3.zip && \
  unzip 2.3.3.zip && rm 2.3.3.zip && cd stp-2.3.3 && mkdir build && \
  cd build && cmake .. && make && make install

# Build and install ucLibc
RUN wget https://github.com/klee/klee-uclibc/archive/klee_uclibc_v1.2.zip && \
  unzip klee_uclibc_v1.2.zip && rm klee_uclibc_v1.2.zip && \
  cd klee-uclibc-klee_uclibc_v1.2 && ./configure --make-llvm-lib  && make -j2

# Build and install Klee
RUN wget https://github.com/klee/klee/archive/v2.0.zip && unzip v2.0.zip && \
  rm v2.0.zip && cd klee-2.0 && mkdir build && cd build && cmake \
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


# Download Tigress
RUN wget https://github.com/elm3nt/table/raw/d1ba4bf5e4da0f24ccca6e35d242ee7e7d8a9dd4/tigress-Linux-x86_64-2.2.zip && \
  unzip tigress-Linux-x86_64-2.2.zip && rm tigress-Linux-x86_64-2.2.zip
# Tigress requires older version of GCC
RUN sudo rm /usr/bin/gcc && sudo ln -s /usr/bin/gcc-4.8 /usr/bin/gcc
# Tigress requires environment variable
RUN echo 'export TIGRESS_HOME=/home/argon/tools/tigress-2.2' >> /home/argon/.bashrc

# Install Argon
RUN wget https://github.com/elm3nt/argon-cli/archive/v0.1.1.zip && unzip v0.1.1.zip && \
  rm v0.1.1.zip
RUN sudo pip3 install -U -r /home/argon/tools/argon-cli-0.1.1/requirements.txt

# Add path of Argon, Tigress and Klee
RUN echo 'export PATH=$PATH:/home/argon/tools/tigress-2.2' >> /home/argon/.bashrc
RUN echo 'export PATH=$PATH:/home/argon/tools/argon-cli-0.1.1' >> /home/argon/.bashrc
RUN echo 'export PATH=$PATH:/home/argon/tools/klee-2.0/build/bin' >> /home/argon/.bashrc

# Update user and permissions
USER argon
WORKDIR /home/argon
RUN sudo chown argon:argon /home/argon/tools/ -R
