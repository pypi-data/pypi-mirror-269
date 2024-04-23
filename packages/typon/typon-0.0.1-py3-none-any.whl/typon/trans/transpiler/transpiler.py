# coding: utf-8
import ast
from pathlib import Path

import colorama

from logging import debug
import colorful as cf

from transpiler import error_display
from transpiler.phases.desugar_compare import DesugarCompare
from transpiler.phases.desugar_op import DesugarOp
from transpiler.phases.desugar_subscript import DesugarSubscript
from transpiler.phases.desugar_with import DesugarWith
from transpiler.phases.emit_cpp.module import emit_module
from transpiler.phases.emit_cpp.visitors import NodeVisitor
from transpiler.phases.if_main import IfMainVisitor
from transpiler.phases.typing import PRELUDE
from transpiler.phases.typing.modules import parse_module
from transpiler.phases.typing.stdlib import StdlibVisitor

TYPON_STD = Path(__file__).parent.parent / "stdlib"

def init():
    error_display.init()
    colorama.init()

    #discover_module(typon_std, PRELUDE.child(ScopeKind.GLOBAL))
    parse_module("builtins", [TYPON_STD], PRELUDE)



def transpile(source, name: str, path: Path):
    __TB__ = f"transpiling module {cf.white(name)}"

    def preprocess(node):
        IfMainVisitor().visit(node)
        node = DesugarWith().visit(node)
        node = DesugarCompare().visit(node)
        node = DesugarOp().visit(node)
        node = DesugarSubscript().visit(node)
        return node

    module = parse_module(path.stem, [path.parent, TYPON_STD], preprocess=preprocess)

    def disp_scope(scope, indent=0):
        debug("  " * indent, scope.kind)
        for child in scope.children:
            disp_scope(child, indent + 1)
        for var in scope.vars.items():
            debug("  " * (indent + 1), var)

    StdlibVisitor([], module.block_data.scope).expr().visit(ast.parse("main()", mode="eval").body)

    def main_module():
        yield from emit_module(module)
        yield "#ifdef TYPON_EXTENSION"
        yield f"PYBIND11_MODULE({module.name()}, m) {{"
        yield f"m.doc() = \"Typon extension module '{module.name()}'\";"
        for n, f in module.fields.items():
            if not f.in_class_def:
                continue
            node = f.from_node
            if getattr(node, "is_main", False):
                continue
            if isinstance(node, ast.FunctionDef):
                if (exports := getattr(f.type, "pybind_exports", None)) is not None:
                    yield f'm.def("{n}", []('
                    for i, ty in enumerate(exports):
                        if i != 0:
                            yield ","
                        yield from NodeVisitor().visit_BaseType(ty)
                        yield f"arg{i}"
                    yield ") {"
                    yield f"return PROGRAMNS::{module.name()}.{node.name}("
                    for i, _ in enumerate(exports):
                        if i != 0:
                            yield ","
                        yield f"arg{i}"
                    yield ").call(); });"
        # visitor = ModuleVisitorExt(self.scope)
        # code = [line for stmt in node.body for line in visitor.visit(stmt)]
        # yield from code
        yield "}"
        yield "#else"
        yield "typon::Root root() {"
        yield f"co_await dot(PROGRAMNS::{module.name()}, main)();"
        yield "}"
        yield "int main(int argc, char* argv[]) {"
        yield "py_sys::all.argv = typon::TyList__oo<>::Obj(std::vector<typon::TyStr__oo<>::Obj>(argv, argv + argc));"
        yield f"root().call();"
        yield "}"
        yield "#endif"

    code = main_module()
    code = filter(None, code)
    code = list(code)
    code = "\n".join(code)
    return code


    exit()

    assert isinstance(res, ast.Module)
    res.name = "__main__"

    code = "\n".join(filter(None, map(str, FileVisitor(Scope(), name).visit(res))))
    return code

init()