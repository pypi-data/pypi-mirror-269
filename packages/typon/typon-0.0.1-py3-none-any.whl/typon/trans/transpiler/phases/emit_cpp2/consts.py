# coding: utf-8
import ast

SYMBOLS = {
    ast.Eq: "==",
    ast.NotEq: '!=',
    ast.Pass: '/* pass */',
    ast.Mult: '*',
    ast.Add: '+',
    ast.Sub: '-',
    ast.Div: '/',
    ast.FloorDiv: '/',  # TODO
    ast.Mod: '%',
    ast.Lt: '<',
    ast.Gt: '>',
    ast.GtE: '>=',
    ast.LtE: '<=',
    ast.LShift: '<<',
    ast.RShift: '>>',
    ast.BitXor: '^',
    ast.BitOr: '|',
    ast.BitAnd: '&',
    ast.Not: '!',
    ast.IsNot: '!=',
    ast.USub: '-',
    ast.And: '&&',
    ast.Or: '||'
}
"""Mapping of Python AST nodes to C++ symbols."""

DUNDER_SYMBOLS = {
    "__eq__": "==",
    "__ne__": "!=",
    "__lt__": "<",
    "__gt__": ">",
    "__ge__": ">=",
    "__le__": "<=",
    "__add__": "+",
    "__sub__": "-",
    "__mul__": "*",
    "__div__": "/",
    "__mod__": "%",
    "__lshift__": "<<",
    "__rshift__": ">>",
    "__xor__": "^",
    "__or__": "|",
    "__and__": "&",
    "__invert__": "~",
    "__neg__": "-",
    "__pos__": "+",
}

PRECEDENCE = [
    ("()", "[]", ".",),
    ("unary", "co_await"),
    ("*", "/", "%",),
    ("+", "-"),
    ("<<", ">>"),
    ("<", "<=", ">", ">="),
    ("==", "!="),
    ("&",),
    ("^",),
    ("|",),
    ("&&",),
    ("||",),
    ("?:", "co_yield"),
    (",",)
]
"""Precedence of C++ operators."""

PRECEDENCE_LEVELS = {op: i for i, ops in enumerate(PRECEDENCE) for op in ops}
"""Mapping of C++ operators to their precedence level."""

MAPPINGS = {
    "True": "typon::TyBool(true)",
    "False": "typon::TyBool(false)",
    "None": "typon::TyNone{}",
    "operator": "operator_",
}
"""Mapping of Python builtin constants to C++ equivalents."""
