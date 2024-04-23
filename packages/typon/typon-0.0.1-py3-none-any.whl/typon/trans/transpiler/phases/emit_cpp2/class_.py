# coding: utf-8
import ast
from typing import Iterable

from dataclasses import dataclass
from transpiler.phases.typing.scope import Scope
from transpiler.phases.emit_cpp import NodeVisitor, FunctionEmissionKind


class ClassVisitor(NodeVisitor):
    def visit_ClassDef(self, node: ast.ClassDef) -> Iterable[str]:
        if gen_instances := getattr(node, "gen_instances", None):
            for args, inst in gen_instances.items():
                yield from self.visit_ClassDef(inst)
            return

        yield f"struct {node.name}_s;"
        yield f"extern {node.name}_s {node.name};"
        yield f"struct {node.name}_s {{"

        yield "struct py_type {"
        inner = ClassInnerVisitor(node.inner_scope)
        for stmt in node.body:
            yield from inner.visit(stmt)

        yield "template<typename... T> py_type(T&&... args) {"
        yield "__init__(this, std::forward<T>(args)...);"
        yield "}"
        yield "py_type() {}"
        yield "py_type(const py_type&) = delete;"
        yield "py_type(py_type&&) = delete;"

        if getattr(node.type, "is_enum", False):
            yield "int value;"
            yield "operator int() const { return value; }"
            yield "void py_repr(std::ostream &s) const {"
            yield f's << "{node.name}.";'
            yield "}"
        else:
            yield "void py_repr(std::ostream &s) const {"
            yield f's << "{node.name}(";'
            for i, (name, memb) in enumerate(node.type.get_members().items()):
                if i != 0:
                    yield 's << ", ";'
                yield f's << "{name}=";'
                yield f"repr_to({name}, s);"
            yield "s << ')';"
            yield "}"

        yield "void py_print(std::ostream &s) const {"
        yield "py_repr(s);"
        yield "}"

        yield "};"

        yield "template<typename... T> auto operator()(T&&... args) {"
        yield "return tyObj<py_type>(std::forward<T>(args)...);"
        yield "}"

        # outer = ClassOuterVisitor(node.inner_scope)
        # for stmt in node.body:
        #     yield from outer.visit(stmt)

        yield f"}} {node.name};"

@dataclass
class ClassInnerVisitor(NodeVisitor):
    scope: Scope

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Iterable[str]:
        member = self.scope.obj_type.fields[node.target.id]
        yield from self.visit(member.type)
        yield node.target.id
        yield ";"

    def visit_Assign(self, node: ast.Assign) -> Iterable[str]:
        yield "static constexpr"
        from transpiler.phases.emit_cpp.block import BlockVisitor
        yield from BlockVisitor(self.scope).visit_Assign(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
        # yield "struct {"
        # yield "type* self;"
        # from transpiler.phases.emit_cpp.block import BlockVisitor
        # yield from BlockVisitor(self.scope).visit_func_new(node, FunctionEmissionKind.METHOD, True)
        # yield f"}} {node.name} {{ this }};"
        yield f"struct {node.name}_m_s : referencemodel::method {{"
        from transpiler.phases.emit_cpp.block import BlockVisitor
        yield from BlockVisitor(self.scope).visit_func_new(node, FunctionEmissionKind.METHOD)
        yield f"}} static constexpr {node.name} {{}};"
        yield ""

@dataclass
class ClassOuterVisitor(NodeVisitor):
    scope: Scope

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Iterable[str]:
        yield ""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
        yield "struct {"
        yield "template<typename Self, typename... T>"
        yield "auto operator()(Self self, T&&... args) {"
        yield f"return dotp(self, {node.name})(std::forward<T>(args)...);"
        yield "}"
        yield f"}} {node.name};"
        yield ""
        # yield "struct : function {"
        # from transpiler.phases.emit_cpp.block import BlockVisitor
        # yield from BlockVisitor(self.scope).visit_func_new(node, FunctionEmissionKind.METHOD)
        # yield f"}} static constexpr {node.name} {{}};"

@dataclass
class ClassInnerVisitor2(NodeVisitor):
    scope: Scope

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Iterable[str]:
        yield ""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
        yield "struct : referencemodel::method {"
        from transpiler.phases.emit_cpp.block import BlockVisitor
        yield from BlockVisitor(self.scope).visit_func_new(node, FunctionEmissionKind.METHOD)
        yield f"}} static constexpr {node.name} {{}};"

@dataclass
class ClassInnerVisitor4(NodeVisitor):
    scope: Scope

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Iterable[str]:
        member = self.scope.obj_type.fields[node.target.id]
        yield from self.visit(member.type)
        yield node.target.id
        yield ";"

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
        yield ""