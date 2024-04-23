import ast
from enum import Flag
from itertools import chain
from typing import Iterable

import transpiler.phases.typing.types as types
from transpiler.phases.typing.exceptions import UnresolvedTypeVariableError
from transpiler.phases.typing.types import BaseType
from transpiler.utils import UnsupportedNodeError, highlight

MAPPINGS = {
    "int": "typon::TyInt"
}

class UniversalVisitor:
    def visit(self, node):
        """Visit a node."""
        __TB__ = f"emitting C++ code for {highlight(node)}"
        # __TB_SKIP__ = True

        if orig := getattr(node, "orig_node", None):
            node = orig

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
            # return f"py_{name[2:-2]}"
            return f"oo{name}oo"
        return MAPPINGS.get(name, name)

    def visit_BaseType(self, node: BaseType) -> Iterable[str]:
        node = node.resolve()

        match node:
            case types.TY_INT:
                yield "decltype(0_pi)"
            case types.TY_FLOAT:
                yield "double"
            case types.TY_BOOL:
                yield "decltype(typon::TyBool(true))"
            case types.TY_NONE:
                yield "typon::TyNone"
            case types.TY_STR:
                yield 'decltype(""_ps)'
            case types.TY_LIST:
                yield "typon::TyList__oo<>::Obj"
            case types.TY_DICT:
                yield "typon::TyDict__oo<>::Obj"
            case types.TypeVariable(name, emit_as_is=em, decltype_str=dt):
                if em:
                    yield name
                elif dt:
                    yield dt
                else:
                    raise UnresolvedTypeVariableError(node)
                    yield f"$VAR__{name}"

                #raise UnresolvedTypeVariableError(node)
            case types.GenericInstanceType():
                yield from self.visit(node.generic_parent)
                yield "<"
                if node.generic_args:
                    yield from join(",", map(self.visit, node.generic_args))
                else:
                    yield "void"
                yield ">"
            # case types.TY_LIST:
            #     yield "typon::TyList"
            # case types.TY_DICT:
            #     yield "typon::TyDict"
            # case types.TY_SET:
            #     yield "typon::TySet"
            case types.TY_TASK:
                yield "typon::Task"
            case types.TY_JOIN:
                yield "typon::Join"
            case types.TY_FORKED:
                yield "typon::Forked"
            case types.TY_MUTEX:
                yield "typon::ArcMutex"
            # TODO: these are nice but don't work perfectly so they break tests
            # case types.UserGenericType():
            #     yield f"typename decltype({node.name()})::Obj"
            # case types.BuiltinType():
            #     yield f"typename std::remove_reference<decltype({node.name()})>::type::Obj"
            case _:
                raise NotImplementedError(node)

def join(sep: str, items: Iterable[Iterable[str]]) -> Iterable[str]:
    items = iter(items)
    try:
        it = next(items)
        if type(it) is str:
            yield it
        else:
            yield from it
        for item in items:
            yield sep
            it = item
            if type(it) is str:
                yield it
            else:
                yield from it
    except StopIteration:
        return


def flatmap(f, items):
    return chain.from_iterable(map(f, items))

class CoroutineMode(Flag):
    SYNC = 1
    FAKE = 2 | SYNC
    ASYNC = 4
    GENERATOR = 8 | ASYNC
    TASK = 16 | ASYNC
    JOIN = 32 | ASYNC