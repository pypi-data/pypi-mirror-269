# coding: utf-8
import ast
from dataclasses import dataclass
from typing import Iterable

from transpiler.phases.emit_cpp.block import BlockVisitor
from transpiler.phases.emit_cpp.module import ModuleVisitor, ModuleVisitor2, ModuleVisitorExt, ModuleVisitor3, \
    ModuleVisitor4


# noinspection PyPep8Naming
@dataclass
class FileVisitor(BlockVisitor):
    module_name: str

    def visit_Module(self, node: ast.Module) -> Iterable[str]:
        __TB__ = "emitting C++ code for Python module"

        stmt: ast.AST
        yield "#include <python/builtins.hpp>"
        yield "#include <python/sys.hpp>"
        visitor = ModuleVisitor(self.scope)
        code = [line for stmt in node.body for line in visitor.visit(stmt)]
        yield from visitor.includes
        yield "namespace PROGRAMNS {"
        yield "template <typename _Unused = void>"
        yield f"struct {node.name}__oo : referencemodel::moduletype<{node.name}__oo<>> {{"
        yield from code

        # visitor = ModuleVisitor2(self.scope)
        # code = [line for stmt in node.body for line in visitor.visit(stmt)]
        # yield from code



        visitor = ModuleVisitor4(self.scope)
        code = [line for stmt in node.body for line in visitor.visit(stmt)]
        yield from code


        visitor = ModuleVisitor3(self.scope)
        code = [line for stmt in node.body for line in visitor.visit(stmt)]
        yield from code

        yield "};"
        yield f"constexpr {node.name}__oo<> {node.name};"
        yield f"static_assert(sizeof {node.name} == 1);"
        yield "}"
        yield "#ifdef TYPON_EXTENSION"
        yield f"PYBIND11_MODULE({self.module_name}, m) {{"
        yield f"m.doc() = \"Typon extension module '{self.module_name}'\";"
        visitor = ModuleVisitorExt(self.scope)
        code = [line for stmt in node.body for line in visitor.visit(stmt)]
        yield from code
        yield "}"
        yield "#else"
        yield "int main(int argc, char* argv[]) {"
        yield "py_sys::all.argv = typon::TyList<TyStr>(std::vector<TyStr>(argv, argv + argc));"
        yield "PROGRAMNS::__main__.root().call();"
        yield "}"
        yield "#endif"
