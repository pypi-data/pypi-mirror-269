# Typon compiler

Typon is a two-part project to bring practical GIL-free concurrency to Python:
1. [`typon-concurrency`](https://lab.nexedi.com/typon/typon-concurrency), a C++ concurrency runtime
2. typon-compiler (this repository), a compiler from Python syntax into C++

## Directory structure

### `docs`, documentation

Currently using Sphinx.

### `include`, standard library and compiler primitives/intrisics

TODO.

### `runtime`, concurrency runtime (Git submodule)

See the [runtime repository](https://lab.nexedi.com/typon/typon-concurrency).

### `trans`, transpiler 

This repository, TODO.

## Getting started

```bash
git clone https://lab.nexedi.com/typon/typon-compiler.git --recursive
python3 -m venv typenv
source typenv/bin/activate
pip install ./typon-compiler
apt install libfmt-dev liburing-dev python3.12-dev libssl-dev
```

## Basic usage

Typon can be used from the command-line to compile a Python file:

```
typon [-o/--output output] [-d/--debug] [-v/--verbose] input
```

Once generated, the C++ code file can be compiled using your compiler of choice:

```
$(CXX) -O3 input.cpp $(typon --cpp-flags) 
```

Currently, you'll get the best support with G++ 13.

## Test harness

`cd` into the `trans` directory, set up your `.env` file (you can copy the `.env.example` file), and run `python3 test_runner.py`.
