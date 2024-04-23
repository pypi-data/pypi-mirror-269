"""
usage:
typon --cpp-flags
or
typon in.py [-o out.py] [-v]
"""

import argparse
import logging
import os
from pathlib import Path
import sys

def main():
    compiler_path = Path(__file__).parent
    stdlib_path = compiler_path.parent / "include"
    runtime_path = compiler_path.parent / "runtime" / "rt" / "include"
    
    sys.path.insert(0, str(compiler_path))
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("input", help="input file", nargs="?" if "--cpp-flags" in sys.argv else 1)
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-e", "--extension", help="generate binding code to allow importing this from CPython", action="store_true")
    parser.add_argument("--cpp-flags", help="print cpp flags", action="store_true")
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    
    if args.cpp_flags:
        import pybind11.commands
        import sysconfig
    
        include_dirs = [
            str(stdlib_path),
            str(runtime_path),
            sysconfig.get_path("include"),
            sysconfig.get_path("platinclude"),
            pybind11.commands.get_include()
        ]
        include_dirs = list(dict.fromkeys(include_dirs))
        # get python major and minor version
        python_version = sys.version_info
        cpp_flags = [
            *["-I" + d for d in include_dirs],
            "-pthread", "-luring", "-lfmt", "-lssl", "-lcrypto", f"-lpython{python_version.major}.{python_version.minor}", "-std=c++20"
        ]
        if args.extension:
            cpp_flags.extend(("-DTYPON_EXTENSION", "-fPIC", "-shared"))
        print(" ".join(cpp_flags))
        exit(0)
    
    path = Path(args.input[0])
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    
    from transpiler.transpiler import transpile
    from transpiler.format import format_code
    
    raw_cpp = transpile(code, path.stem, path)
    formatted = format_code(raw_cpp)
    
    output_name = args.output or path.with_suffix('.cpp')
    
    with open(output_name, "w", encoding="utf-8") as f:
        f.write(formatted)

# TODO
"""
webserver => investiguer
scanfs => fork
promesse => faire
self/this => bind/dot
stocker smart ptr dans closures
"""
