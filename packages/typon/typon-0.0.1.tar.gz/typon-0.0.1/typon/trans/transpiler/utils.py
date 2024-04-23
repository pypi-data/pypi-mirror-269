# coding: utf-8
import ast
from dataclasses import dataclass
from itertools import zip_longest
from typing import Union
import colorful as cf
from pygments.token import *

#
# from colorama import Fore, Back
# from colorama.ansi import AnsiCodes
#
#
# class AnsiStyle(AnsiCodes):
#     BOLD = 1
#     DIM = 2
#     ITALIC = 3
#     UNDERLINE = 4
#     BLINK = 5
#     REVERSE = 7
#     HIDDEN = 8
#     STRIKETHROUGH = 9
#
#     RESET = "21;22;23;24;25;27;28;29"
#
# Style = AnsiStyle()

COLOR_SCHEME = {
    Token:              ('',            ''),

    Whitespace:         ('gray',   'brightblack'),
    Comment:            ('brightblack',   'brightblack'),
    Comment.Preproc:    ('cyan',        'brightcyan'),
    Keyword:            ('brightblue',    'brightblue'),
    Keyword.Type:       ('cyan',        'brightcyan'),
    Operator.Word:      ('magenta',      'brightmagenta'),
    Name.Builtin:       ('cyan',        'brightcyan'),
    Name.Function:      ('green',   'brightgreen'),
    Name.Namespace:     ('brightcyan',      'brightcyan'),
    Name.Class:         ('green', 'brightgreen'),
    Name.Exception:     ('cyan',        'brightcyan'),
    Name.Decorator:     ('brightblack',    'gray'),
    Name.Variable:      ('red',     'brightred'),
    Name.Constant:      ('red',     'brightred'),
    Name.Attribute:     ('cyan',        'brightcyan'),
    Name.Tag:           ('brightblue',        'brightblue'),
    String:             ('yellow',       'yellow'),
    Number:             ('brightmagenta',    'brightblue'),

    Generic.Deleted:    ('brightred',        'brightred'),
    Generic.Inserted:   ('green',  'brightgreen'),
    Generic.Heading:    ('**',         '**'),
    Generic.Subheading: ('*magenta*',   '*brightmagenta*'),
    Generic.Prompt:     ('**',         '**'),
    Generic.Error:      ('brightred',        'brightred'),

    Error:              ('brightred',      'brightred'),
}

def highlight(code, full=False):
    """
    Syntax highlights code as Python using colorama
    """
    __TB__ = f"syntax highlighting {code}"
    if code is None:
        return cf.yellow("<None>")
    if type(code) == list:
        return repr([highlight(x) for x in code])
    from transpiler.phases.typing.types import BaseType
    if isinstance(code, ast.AST):
        return cf.italic_grey60(f"[{type(code).__name__}] ") + highlight(ast.unparse(code))
    elif isinstance(code, BaseType):
        return cf.italic_grey60(f"[{type(code).__name__}] ") + highlight(str(code))
    from pygments import highlight as pyg_highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import TerminalFormatter

    lexer = get_lexer_by_name("python", stripnl=False)
    items = pyg_highlight(code, lexer, TerminalFormatter(colorscheme=COLOR_SCHEME)).replace("\x1b[39;49;00m", "\x1b[39m")
    if full:
        return items
    items = items.splitlines()
    res = items[0]
    if len(items) > 1:
        res += cf.white(" [...]")
    return f"\x1b[39;49m{cf.on_gray23(res)}"


def compare_ast(node1: Union[ast.expr, list[ast.expr]], node2: Union[ast.expr, list[ast.expr]]) -> bool:
    if type(node1) is not type(node2):
        return False

    if isinstance(node1, ast.AST):
        for k, v in vars(node1).items():
            if k in {"lineno", "end_lineno", "col_offset", "end_col_offset", "ctx", "type"}:
                continue
            if not compare_ast(v, getattr(node2, k)):
                return False
        return True

    elif isinstance(node1, list) and isinstance(node2, list):
        return all(compare_ast(n1, n2) for n1, n2 in zip_longest(node1, node2))
    else:
        return node1 == node2


@dataclass
class UnsupportedNodeError(Exception):
    node: ast.AST

    def __str__(self) -> str:
        return f"Unsupported node: {self.node.__class__.__mro__} {ast.dump(self.node)}"

def linenodata(node):
    return {k: getattr(node, k) for k in ("lineno", "end_lineno", "col_offset", "end_col_offset")}