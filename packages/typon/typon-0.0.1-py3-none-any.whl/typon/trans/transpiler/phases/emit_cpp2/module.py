# coding: utf-8
import ast
from typing import Iterable

from dataclasses import dataclass, field

from transpiler.phases.typing import FunctionType
from transpiler.phases.typing.scope import Scope
from transpiler.phases.emit_cpp import CoroutineMode, FunctionEmissionKind, NodeVisitor, join
from transpiler.phases.emit_cpp.block import BlockVisitor
from transpiler.phases.emit_cpp.class_ import ClassVisitor, ClassInnerVisitor, ClassInnerVisitor2, ClassInnerVisitor4
from transpiler.phases.emit_cpp.function import FunctionVisitor
from transpiler.utils import compare_ast, highlight

IGNORED_IMPORTS = {"typon", "typing", "__future__", "dataclasses", "enum"}

# noinspection PyPep8Naming
@dataclass
class ModuleVisitor(BlockVisitor):
    includes: list[str] = field(default_factory=list)
    def visit_Import(self, node: ast.Import) -> Iterable[str]:
        __TB__ = f"emitting C++ code for {highlight(node)}"
        for alias in node.names:
            concrete = self.fix_name(alias.asname or alias.name)
            if alias.module_obj.is_python:
                yield f"namespace py_{concrete} {{"
                yield f"struct {concrete}_t {{"

                for name, obj in alias.module_obj.fields.items():
                    ty = obj.type.resolve()
                    if getattr(ty, "python_func_used", False):
                        yield from self.emit_python_func(alias.name, name, name, ty)

                yield "} all;"
                yield f"auto& get_all() {{ return all; }}"
                yield "}"
                yield f'auto& {concrete} = py_{concrete}::get_all();'
            elif alias.name in IGNORED_IMPORTS:
                yield ""
            else:
                yield from self.import_module(alias.name)
                yield f'auto& {concrete} = py_{alias.name}::get_all();'

    def import_module(self, name: str) -> Iterable[str]:
        self.includes.append(f'#include <python/{name}.hpp>')
        yield ""

    def emit_python_func(self, mod: str, name: str, alias: str, fty: FunctionType) -> Iterable[str]:
        __TB__ = f"emitting C++ code for Python function {highlight(f'{mod}.{name}')}"

        yield "struct {"
        yield f"auto operator()("

        for i, argty in enumerate(fty.parameters):
            if i != 0:
                yield ", "
            yield "lvalue_or_rvalue<"
            yield from self.visit(argty)
            yield f"> arg{i}"

        yield ") {"
        yield "InterpGuard guard{};"
        yield "try {"
        yield f"return py::module_::import(\"{mod}\").attr(\"{name}\")("
        for i, argty in enumerate(fty.parameters):
            if i != 0:
                yield ", "
            yield f"*arg{i}"
        yield ").cast<"
        yield from self.visit(fty.return_type)
        yield ">();"
        yield "} catch (py::error_already_set& e) {"
        yield 'std::cerr << "Python exception: " << e.what() << std::endl;'
        yield "throw;"
        yield "}"
        yield "}"
        yield f"}} {alias};"

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Iterable[str]:
        if node.module in IGNORED_IMPORTS:
            yield ""
        elif node.module_obj.is_python:
            for alias in node.names:
                fty = alias.item_obj.resolve()
                #assert isinstance(fty, FunctionType)

                yield from self.emit_python_func(node.module, alias.name, alias.asname or alias.name, fty)
        else:
            yield from self.import_module(node.module)
            for alias in node.names:
                yield f"auto& {alias.asname or alias.name} = py_{node.module}::get_all().{alias.name};"

    def visit_Expr(self, node: ast.Expr) -> Iterable[str]:
        if isinstance(node.value, ast.Str):
            if "\n" in node.value.s:
                yield f"/*{node.value.s}*/"
            else:
                yield f"//{node.value.s}"
        else:
            raise NotImplementedError(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Iterable[str]:
        #yield from ClassVisitor().visit(node)
        yield from ()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
        yield from super().visit_free_func(node, FunctionEmissionKind.DECLARATION)


@dataclass
class ModuleVisitor2(NodeVisitor):
    scope: Scope
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
        yield from BlockVisitor(self.scope).visit_free_func(node, FunctionEmissionKind.DEFINITION)

    def visit_AST(self, node: ast.AST) -> Iterable[str]:
        yield ""
        pass

@dataclass
class ModuleVisitor3(NodeVisitor):
    scope: Scope
    def visit_ClassDef(self, node: ast.ClassDef) -> Iterable[str]:
        yield from ()
        return
        if gen_instances := getattr(node, "gen_instances", None):
            for args, inst in gen_instances.items():
                yield from self.visit_ClassDef(inst)
            return
        yield f"static constexpr _detail_<__main__>::{node.name}<> {node.name} {{}};"

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
        yield from BlockVisitor(self.scope).visit_free_func(node, FunctionEmissionKind.DEFINITION)

@dataclass
class ModuleVisitor4(NodeVisitor):
    scope: Scope
    def visit_ClassDef(self, node: ast.ClassDef) -> Iterable[str]:
        if gen_instances := getattr(node, "gen_instances", None):
            for args, inst in gen_instances.items():
                yield from self.visit_ClassDef(inst)
            return

        yield f"template <typename _Base0 = referencemodel::object>"
        yield f"struct {node.name}__oo : referencemodel::classtype<_Base0, {node.name}__oo<>> {{"
        yield f"static constexpr std::string_view name = \"{node.name}\";"

        inner = ClassInnerVisitor2(node.inner_scope)
        for stmt in node.body:
            yield from inner.visit(stmt)

        yield f"struct Obj : referencemodel::instance<{node.name}__oo<>, Obj> {{"

        inner = ClassInnerVisitor4(node.inner_scope)
        for stmt in node.body:
            yield from inner.visit(stmt)

        yield "template <typename... U>"
        yield "Obj(U&&... args) {"
        yield "dot(this, __init__)(this, std::forward<U>(args)...);"
        yield "}"


        yield "};"

        yield "template <typename... T>"
        yield "auto operator() (T&&... args) const {"
        yield "return referencemodel::rc(Obj{std::forward<T>(args)...});"
        yield "}"

        yield f"}};"
        yield f"static constexpr {node.name}__oo<> {node.name} {{}};"
        yield f"static_assert(sizeof {node.name} == 1);"

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
        yield from ()

@dataclass
class ModuleVisitorExt(NodeVisitor):
    scope: Scope
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
        if getattr(node, "is_main", False):
            yield from ()
            return
        #yield from BlockVisitor(self.scope).visit_free_func(node, FunctionEmissionKind.DEFINITION)
        #yield f'm.def("{node.name}", CoroWrapper(PROGRAMNS::{node.name}));'
        yield f'm.def("{node.name}", PROGRAMNS::{node.name});'

    def visit_ClassDef(self, node: ast.ClassDef) -> Iterable[str]:
        if gen_instances := getattr(node, "gen_instances", None):
            for args, inst in gen_instances.items():
                yield from self.visit_ClassDef(inst)
            return
        yield f"py::class_<PROGRAMNS::{node.name}_s::py_type>(m, \"{node.name}\")"
        if init := node.type.fields.get("__init__", None):
            init = init.type.resolve().remove_self()
            init_params = init.parameters
            yield ".def(py::init<"
            yield from join(", ", map(self.visit, init_params))
            yield ">())"
        yield f'.def("__repr__", [](const PROGRAMNS::{node.name}_s::py_type& self)'
        yield "{ return repr(self); })"
        for f, v in node.type.fields.items():
            if f == "__init__":
                continue
            if isinstance(v.type, FunctionType):
                meth = v.type.remove_self()
                yield f'.def("{f}", [](const PROGRAMNS::{node.name}_s::py_type& a'
                if meth.parameters:
                    yield ","
                    vis = BlockVisitor(node.scope)
                    yield from vis.visit_func_params(((f"arg{i}", ty, None) for i, ty in enumerate(meth.parameters)), FunctionEmissionKind.LAMBDA)
                yield f') {{ return dotp(&a, {f})('
                if meth.parameters:
                    yield from join(", ", (f"arg{i}" for i, _ in enumerate(meth.parameters)))
                yield ').call(); })'
            else:
                yield f'.def_readwrite("{f}", &PROGRAMNS::{node.name}_s::py_type::{f})'
        yield ";"
        pass

    def visit_AST(self, node: ast.AST) -> Iterable[str]:
        yield from ()
        pass
