# coding: utf-8
import ast
import enum
from enum import Flag
from itertools import chain
from typing import Iterable

from transpiler.phases.emit_cpp.consts import MAPPINGS
from transpiler.phases.typing import TypeVariable
from transpiler.phases.typing.exceptions import UnresolvedTypeVariableError
from transpiler.phases.typing.types import BaseType, TY_INT, TY_BOOL, TY_NONE, Promise, PromiseKind, TY_STR, UserType, \
    TypeType, TypeOperator, TY_FLOAT, FunctionType, UnionType
from transpiler.utils import UnsupportedNodeError, highlight


class UniversalVisitor:
    def visit(self, node):
        """Visit a node."""
        __TB__ = f"emitting C++ code for {highlight(node)}"
        # __TB_SKIP__ = True

        if type(node) == list:
            for n in node:
                yield from self.visit(n)
        else:
            for parent in node.__class__.__mro__:
                if visitor := getattr(self, 'visit_' + parent.__name__, None):
                    yield from visitor(node)
                    break
            else:
                yield from self.missing_impl(node)

    def missing_impl(self, node):
        raise UnsupportedNodeError(node)


class NodeVisitor(UniversalVisitor):
    def process_args(self, node: ast.arguments) -> (str, str, str):
        for field in ("posonlyargs", "vararg", "kwonlyargs", "kw_defaults", "kwarg", "defaults"):
            if getattr(node, field, None):
                raise NotImplementedError(node, field)

        if not node.args:
            return "", "()", []
        f_args = [(self.fix_name(arg.arg), f"T{i + 1}") for i, arg in enumerate(node.args)]
        return (
            "<" + ", ".join(f"typename {t}" for _, t in f_args) + ">",
            "(" + ", ".join(f"{t} {n}" for n, t in f_args) + ")",
            [n for n, _ in f_args]
        )

    def fix_name(self, name: str) -> str:
        if name.startswith("__") and name.endswith("__"):
            return f"py_{name[2:-2]}"
        return MAPPINGS.get(name, name)

    def visit_BaseType(self, node: BaseType) -> Iterable[str]:
        node = node.resolve()
        if node is TY_INT:
            yield "int"
        elif node is TY_FLOAT:
            yield "double"
        elif node is TY_BOOL:
            yield "bool"
        elif node is TY_NONE:
            yield "void"
        elif node is TY_STR:
            yield "TyStr"
        elif isinstance(node, UserType):
            # if node.is_reference:
            #     yield "TyObj<"
            #yield "auto"
            yield f"referencemodel::Rc<__main____oo<>::{node.name}__oo<>::Obj>"
            # if node.is_reference:
            #     yield "::py_type>"
        elif isinstance(node, TypeType):
            yield "auto"  # TODO
        elif isinstance(node, FunctionType):
            yield "std::function<"
            yield from self.visit(node.return_type)
            yield "("
            yield from join(", ", map(self.visit, node.parameters))
            yield ")>"
        elif isinstance(node, Promise):
            yield "typon::"
            if node.kind == PromiseKind.TASK:
                yield "Task"
            elif node.kind == PromiseKind.JOIN:
                yield "Join"
            elif node.kind == PromiseKind.FUTURE:
                yield "Future"
            elif node.kind == PromiseKind.FORKED:
                yield "Forked"
            elif node.kind == PromiseKind.GENERATOR:
                yield "Generator"
            else:
                raise NotImplementedError(node)
            yield "<"
            yield from self.visit(node.return_type)
            yield ">"
        elif isinstance(node, TypeVariable):
            # yield f"TYPEVAR_{node.name}";return
            raise UnresolvedTypeVariableError(node)
        elif isinstance(node, UnionType) and (ty := node.is_optional()):
            yield "std::optional<"
            yield from self.visit(ty)
            yield ">"
        elif isinstance(node, TypeOperator):
            yield "typon::Py" + node.name.title()
            if node.args:
                yield "<"
                yield from join(", ", map(self.visit, node.args))
                yield ">"
        else:
            raise NotImplementedError(node)


class CoroutineMode(Flag):
    SYNC = 1
    FAKE = 2 | SYNC
    ASYNC = 4
    GENERATOR = 8 | ASYNC
    TASK = 16 | ASYNC
    JOIN = 32 | ASYNC


class FunctionEmissionKind(enum.Enum):
    DECLARATION = enum.auto()
    DEFINITION = enum.auto()
    METHOD = enum.auto()
    LAMBDA = enum.auto()


