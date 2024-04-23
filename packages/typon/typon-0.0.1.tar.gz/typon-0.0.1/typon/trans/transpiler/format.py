# coding: utf-8
import subprocess

import clang_format

clang = clang_format._get_executable("clang-format")  # noqa


def format_code(code: str) -> str:
    return subprocess.check_output([
        clang,
        "--style=LLVM",
        "--assume-filename=main.cpp"
    ], input=code.encode("utf-8")).decode("utf-8")
