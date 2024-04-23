# coding: utf-8
import argparse
import concurrent.futures
import enum
import logging
import os
import subprocess
#logging.basicConfig(level=logging.DEBUG)
import sys
from datetime import datetime
from os import system, environ
from pathlib import Path
import colorama
import colorful as cf
import signal

from transpiler.format import format_code

# load .env file
from dotenv import load_dotenv

from transpiler.transpiler import transpile

colorama.init()
load_dotenv()

# todo: promise https://lab.nexedi.com/nexedi/slapos.toolbox/blob/master/slapos/promise/plugin/check_socket_listening.py
# todo: scan fs https://lab.nexedi.com/xavier_thompson/scan-filesystem/blob/master/rust/src/main.rs
# todo: refs https://lab.nexedi.com/xavier_thompson/typon-snippets/tree/master/references

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--compile", action="store_true")
parser.add_argument("-g", "--generate", action="store_true")
parser.add_argument("-o", "--only", nargs="+")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-w", "--workers", type=int, default=max(1, os.cpu_count() - 2))
args = parser.parse_args()

class TestStatus(enum.Enum):
    SUCCESS = 0
    TYPON_ERROR = 1
    CLANG_ERROR = 2  # returned from ALT_RUNNER
    RUNTIME_ERROR = 3  # returned from ALT_RUNNER
    SKIPPED = 4
    PYTHON_ERROR = 5
    TIMEOUT = 6
    NOT_RAN = 7

    def ascii(self):
        color, msg = {
            TestStatus.SUCCESS: (cf.green, "✓"),
            TestStatus.NOT_RAN: (cf.green, "✓ built"),
            TestStatus.TYPON_ERROR: (cf.red, "Typon"),
            TestStatus.CLANG_ERROR: (cf.red, "C++"),
            TestStatus.RUNTIME_ERROR: (cf.red, "Run"),
            TestStatus.SKIPPED: (cf.yellow, "Skipped"),
            TestStatus.PYTHON_ERROR: (cf.red, "Python"),
            TestStatus.TIMEOUT: (cf.red, "Timeout"),
        }[self]
        return color("{:^7s}".format(msg))

def exec_cmd(cmd):
    try:
        return subprocess.run(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr, timeout=200).returncode
    except subprocess.TimeoutExpired:
        return TestStatus.TIMEOUT

def run_test(path, quiet=True):
    if quiet:
        sys.stdout = open(path.with_suffix(".out"), 'w')
        sys.stderr = open(path.with_suffix(".err"), 'w')
    print("** Running", path)
    if path.name.startswith('_'):
        print("Skipping")
        return TestStatus.SKIPPED
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
        execute = "# norun" not in code
        compile = "# nocompile" not in code
        extension = "# extension" in code
        try:
            res = format_code(transpile(code, path.stem, path))
        except:
            if not quiet:
                raise
            return TestStatus.TYPON_ERROR
    name_cpp = path.with_suffix('.cpp')
    with open(name_cpp, "w", encoding="utf-8") as fcpp:
        fcpp.write(res)
    if args.compile:
        return TestStatus.SUCCESS
    execute_str = "true" if (execute and not args.generate) else "false"
    name_bin = path.with_suffix("").as_posix() + ("\\$(python3.12-config --extension-suffix)" if extension else ".exe")
    if exec_cmd(f'bash -c "export PYTHONPATH=stdlib; if {execute_str}; then echo python3.12 ./{path.as_posix()}; fi"') != 0:
        return TestStatus.PYTHON_ERROR
    if compile and (alt := environ.get("ALT_RUNNER")):
        if (code := exec_cmd(alt.format(
                name_bin=name_bin,
                name_cpp_posix=name_cpp.as_posix(),
                run_file=execute_str,
                test_exec=f"python3.12 {path.with_suffix('.post.py').as_posix()}" if extension else name_bin,
                bonus_flags="-e" if extension else ""
        ))) != 0:
            return TestStatus(code)
    else:
        print("no ALT_RUNNER")
    return TestStatus.SUCCESS

def runner(path):
    start = datetime.now()
    result = run_test(path)
    duration = datetime.now() - start
    return path, result, duration

def sigint_handler(signum, frame):
    sys.exit(1)

signal.signal(signal.SIGINT, sigint_handler)

def run_tests():
    tests = sorted(Path('tests').glob('*.py'))
    tests = [t for t in tests if ".post." not in t.name]
    if args.only:
        tests = [p for p in tests if p.stem in args.only]
    if args.verbose:
        for path in tests:
            run_test(path, False)
    else:
        pool = concurrent.futures.ProcessPoolExecutor(args.workers)
        print("Running", len(tests), "tests as", pool._max_workers, "workers")
        start = datetime.now()
        with pool as executor:
            futures = {path: executor.submit(runner, path) for path in tests}
            try:
                for future in concurrent.futures.as_completed(futures.values(), 240):
                    path, status, duration = future.result()
                    print(f"[{status.ascii()}] ({duration.total_seconds():2.2f}s) {path.name}")
            except TimeoutError:
                new_futures = {p: f for p, f in futures.items() if not f.done()}
                print("Timeout,", len(new_futures), "left:", new_futures.keys())
        duration = datetime.now() - start
        print("Done in", duration.total_seconds(), "seconds")


if __name__ == "__main__":
    run_tests()
