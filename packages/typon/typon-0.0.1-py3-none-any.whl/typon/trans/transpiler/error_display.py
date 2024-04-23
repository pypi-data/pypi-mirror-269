# coding: utf-8
import ast
import builtins
import importlib
import inspect
import sys
import traceback
import colorful as cf

from transpiler.exceptions import CompileError
from transpiler.utils import highlight


def exception_hook(exc_type, exc_value, tb):
    print = lambda *args, **kwargs: builtins.print(*args, **kwargs, file=sys.stderr)
    last_node = None
    last_file = None

    orig_tb = tb

    while tb:
        local_vars = tb.tb_frame.f_locals
        name = tb.tb_frame.f_code.co_name

        if name in ("transpile", "parse_module"):
            last_file = local_vars["path"]

        if name == "visit" and (node := local_vars["node"]) and isinstance(node, ast.AST):
            last_node = node

        if node := local_vars.get("__TB_NODE__", None):
            last_node = node

        if local_vars.get("__TB_SKIP__", None) and tb.tb_next:
            tb = tb.tb_next
            continue

        filename = tb.tb_frame.f_code.co_filename
        line_no = tb.tb_lineno
        print(cf.red(f"File {filename}:{line_no}, in {cf.green(name)}"), end="")

        if info := local_vars.get("__TB__", None):
            print(f": {cf.magenta(info)}\x1b[24m")
        else:
            print()
        tb = tb.tb_next

    if last_node is not None and last_file is not None:
        print()
        if not hasattr(last_node, "lineno"):
            print(cf.red("Error:"), cf.white("No line number available"))
            last_node.lineno = 1
            print(ast.unparse(last_node))
        else:
            print(f"In file {cf.white(last_file)}:{last_node.lineno}")
            #print(f"From {last_node.lineno}:{last_node.col_offset} to {last_node.end_lineno}:{last_node.end_col_offset}")
            try:
                with open(last_file, "r", encoding="utf-8") as f:
                    code = f.read()
            except Exception:
                pass
            else:
                hg = (str(highlight(code, True))
                      .replace("\x1b[04m", "")
                      .replace("\x1b[24m", "")
                      .replace("\x1b[39;24m", "\x1b[39m")
                      .splitlines())
                if last_node.lineno == last_node.end_lineno:
                    old = hg[last_node.lineno - 1]
                    start, end = find_indices(old, [last_node.col_offset, last_node.end_col_offset])
                    hg[last_node.lineno - 1] = old[:start] + "\x1b[4m" + old[start:end] + "\x1b[24m" + old[end:]
                else:
                    old = hg[last_node.lineno - 1]
                    [start] = find_indices(old, [last_node.col_offset])
                    hg[last_node.lineno - 1] = old[:start] + "\x1b[4m" + old[start:]
                    for lineid in range(last_node.lineno, last_node.end_lineno - 1):
                        old = hg[lineid]
                        first_nonspace = len(old) - len(old.lstrip())
                        hg[lineid] = old[:first_nonspace] + "\x1b[4m" + old[first_nonspace:] + "\x1b[24m"
                    old = hg[last_node.end_lineno - 1]
                    first_nonspace = len(old) - len(old.lstrip())
                    [end] = find_indices(old, [last_node.end_col_offset])
                    hg[last_node.end_lineno - 1] = old[:first_nonspace] + "\x1b[4m" + old[first_nonspace:end] + "\x1b[24m" + old[end:]
                CONTEXT_SIZE = 2
                start = max(0, last_node.lineno - CONTEXT_SIZE - 1)
                offset = start + 1
                for i, line in enumerate(hg[start:last_node.end_lineno + CONTEXT_SIZE]):
                    erroneous = last_node.lineno <= offset + i <= last_node.end_lineno
                    indicator = cf.white("  →") if erroneous else "   "
                    bar = " ▎"
                    # bar = "│" if erroneous else "┊"
                    disp = f"\x1b[24m{indicator}{cf.white}{(offset + i):>4}{cf.red if erroneous else cf.reset}{bar}{cf.reset} {line}\x1b[24m"
                    print(disp)
                    # print(repr(disp))
    print()
    if isinstance(exc_value, CompileError):
        print(cf.red("Error:"), exc_value)
        detail = inspect.cleandoc(exc_value.detail(last_node))
        if detail:
            print()
            print(detail)
    else:
        print(cf.red("Internal Compiler Error:"), exc_value)
        print()
        print("Please report this error to the Typon maintainers.")
        traceback.print_tb(orig_tb, limit=-1)
    print()

def find_indices(s, indices: list[int]) -> list[int]:
    """
    Matches indices to an ANSI-colored string.

    :param s: An input string. This will usually be a line from a Python file that has been highlighted using Pygments.
    :param indices: A list of indices to match. These will come from the `ast` parser and are UTF-8 *byte* offsets,
                    not *characters*!
    :return: A list of *character* offsets that match the given indices, such text can be inserted at these indices and
             end up in the expected place.
    """
    results = set()
    i = 0
    j = 0
    it = iter(sorted(list(set(indices))))
    current = next(it)
    while i <= len(s):
        if i != len(s) and s[i] == "\x1b":
            i += 1
            while s[i] != "m":
                i += 1
            i += 1
            continue

        if j == current:
            results.add(i)
            try:
                current = next(it)
            except StopIteration:
                break

        j += len(s[i].encode("utf-8"))
        i += 1
    assert len(results) == len(indices), (results, indices, s)
    return sorted(list(results))

assert find_indices("\x1b[48;5;237mmath.abcd\x1b[37m\x1b[39m\x1b[49m", [0, 9]) == [11, 35], find_indices("\x1b[48;5;237mmath.abcd\x1b[37m\x1b[39m\x1b[49m", [0, 9])
assert find_indices("abcdef", [2, 5]) == [2, 5]
assert find_indices("abc\x1b[32mdef", [2, 5]) == [2, 10], find_indices("abc\x1b[32mdef", [2, 5])
assert find_indices("math.abcd\x1b[37m\x1b[39m", [0, 9]) == [0, 19], find_indices("math.abcd\x1b[37m\x1b[39m", [0, 9])
assert find_indices('    \x1b[36mprint\x1b[39m(x, y, z)\x1b[37m\x1b[39m', [4, 18]) == [9, 38], find_indices('    \x1b[36mprint\x1b[39m(x, y, z)\x1b[37m\x1b[39m', [4, 18])

def init():
    sys.excepthook = exception_hook

    try:
        pydevd = importlib.import_module("_pydevd_bundle.pydevd_breakpoints")
    except ImportError:
        pass
    else:
        pydevd._fallback_excepthook = sys.excepthook
        pydevd.original_excepthook = sys.excepthook