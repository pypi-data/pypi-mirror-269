# coding: utf-8
import ast
from dataclasses import dataclass, field
from typing import Iterable, Optional

from transpiler.phases.typing.common import is_builtin
from transpiler.phases.typing.scope import Scope
from transpiler.phases.typing.types import BaseType, TY_INT, TY_BOOL, TypeVariable
from transpiler.utils import compare_ast
from transpiler.phases.emit_cpp import NodeVisitor, CoroutineMode, flatmap, FunctionEmissionKind
from transpiler.phases.emit_cpp.expr import ExpressionVisitor
from transpiler.phases.emit_cpp.search import SearchVisitor

#from transpiler.scope import VarDecl, VarKind, Scope


# noinspection PyPep8Naming
@dataclass
class BlockVisitor(NodeVisitor):
    scope: Scope
    generator: CoroutineMode = field(default=CoroutineMode.SYNC, kw_only=True)

    def expr(self) -> ExpressionVisitor:
        return ExpressionVisitor(self.scope, self.generator)

    def visit_Pass(self, node: ast.Pass) -> Iterable[str]:
        yield ";"

    # def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
    #     yield from self.visit_free_func(node)

    def visit_free_func(self, node: ast.FunctionDef, emission: FunctionEmissionKind) -> Iterable[str]:
        if getattr(node, "is_main", False):
            if emission == FunctionEmissionKind.DECLARATION:
                return
            # Special case handling for Python's interesting way of defining an entry point.
            # I mean, it's not *that* bad, it's just an attempt at retrofitting an "entry point" logic in a scripting
            # language that, by essence, uses "the start of the file" as the implicit entry point, since files are
            # read and executed line-by-line, contrary to usual structured languages that mark a distinction between
            # declarations (functions, classes, modules, ...) and code.
            # Also, for nitpickers, the C++ standard explicitly allows for omitting a `return` statement in the `main`.
            # 0 is returned by default.
            yield "typon::Root root() const"

            def block():
                yield from node.body
                yield ast.Return()

            from transpiler.phases.emit_cpp.function import FunctionVisitor
            yield "{"
            yield from self.visit_func_decls(block(), node.scope, CoroutineMode.TASK)
            yield "}"
            return

        if emission == FunctionEmissionKind.DECLARATION:
            yield f"struct {node.name}_inner {{"
        yield from self.visit_func_new(node, emission)
        if emission == FunctionEmissionKind.DECLARATION:
            yield f"}} {node.name};"

    def visit_func_decls(self, body: list[ast.stmt], inner_scope: Scope, mode = CoroutineMode.ASYNC) -> Iterable[str]:
        for child in body:
            from transpiler.phases.emit_cpp.function import FunctionVisitor
            child_visitor = FunctionVisitor(inner_scope, generator=mode)

            for name, decl in getattr(child, "decls", {}).items():
                #yield f"decltype({' '.join(self.expr().visit(decl.type))}) {name};"
                yield from self.visit(decl.type)
                yield f" {name};"
            yield from child_visitor.visit(child)

    def visit_func_params(self, args: Iterable[tuple[str, BaseType, Optional[ast.expr]]], emission: FunctionEmissionKind) -> Iterable[str]:
        for i, (arg, argty, default) in enumerate(args):
            if i != 0:
                yield ", "
            if emission == FunctionEmissionKind.METHOD and i == 0:
                yield "Self"
            else:
                yield from self.visit(argty)
            yield arg
            if emission in {FunctionEmissionKind.DECLARATION, FunctionEmissionKind.LAMBDA, FunctionEmissionKind.METHOD} and default:
                yield " = "
                yield from self.expr().visit(default)

    def visit_func_new(self, node: ast.FunctionDef, emission: FunctionEmissionKind, skip_first_arg: bool = False) -> Iterable[str]:
        if emission == FunctionEmissionKind.LAMBDA:
            yield "[&]"
        else:
            if emission == FunctionEmissionKind.METHOD:
                yield "template <typename Self>"
            yield from self.visit(node.type.return_type)
            if emission == FunctionEmissionKind.DEFINITION:
                yield f"{node.name}_inner::"
            yield "operator()"
        yield "("
        padded_defaults = [None] * (len(node.args.args) if node.type.optional_at is None else node.type.optional_at) + node.args.defaults
        args_iter = zip(node.args.args, node.type.parameters, padded_defaults)
        if skip_first_arg:
            next(args_iter)
        yield from self.visit_func_params(((arg.arg, argty, default) for arg, argty, default in args_iter), emission)
        yield ")"

        if emission == FunctionEmissionKind.METHOD:
            yield "const"

        inner_scope = node.inner_scope

        if emission == FunctionEmissionKind.DECLARATION:
            yield ";"
            return

        if emission == FunctionEmissionKind.LAMBDA:
            yield "->"
            yield from self.visit(node.type.return_type)

        yield "{"

        class ReturnVisitor(SearchVisitor):
            def visit_Return(self, node: ast.Return) -> bool:
                yield True

            def visit_Yield(self, node: ast.Yield) -> bool:
                yield True

            def visit_FunctionDef(self, node: ast.FunctionDef):
                yield from ()

            def visit_ClassDef(self, node: ast.ClassDef):
                yield from ()

        has_return = ReturnVisitor().match(node.body)

        yield from self.visit_func_decls(node.body, inner_scope)

        if not has_return and isinstance(node.type.return_type, Promise):
            yield "co_return;"

        yield "}"

    def visit_lvalue(self, lvalue: ast.expr, declare: bool | list[bool] = False) -> Iterable[str]:
        if isinstance(lvalue, ast.Tuple):
            for name, decl, ty in zip(lvalue.elts, declare, lvalue.type.args):
                if decl:
                    yield from self.visit_lvalue(name, True)
                    yield ";"
            yield f"std::tie({', '.join(flatmap(self.visit_lvalue, lvalue.elts))})"
        elif isinstance(lvalue, ast.Name):
            if lvalue.id == "_":
                if not declare:
                    yield "std::ignore"
                return
            name = self.fix_name(lvalue.id)
            # if name not in self._scope.vars:
            # if not self.scope.exists_local(name):
            #     yield self.scope.declare(name, (" ".join(self.expr().visit(val)), val) if val else None,
            #                              getattr(val, "is_future", False))
            if declare:
                yield from self.visit(lvalue.type)
            yield name
        elif isinstance(lvalue, ast.Subscript):
            yield from self.expr().visit(lvalue)
        elif isinstance(lvalue, ast.Attribute):
            yield from self.expr().visit(lvalue)
        else:
            raise NotImplementedError(lvalue)

    def visit_Assign(self, node: ast.Assign) -> Iterable[str]:
        if len(node.targets) != 1:
            raise NotImplementedError(node)
        if isinstance(node.targets[0].type, TypeType) and isinstance(node.targets[0].type.type_object, TypeVariable):
            yield from ()
            return
        #if node.value.type
        yield from self.visit_lvalue(node.targets[0], node.is_declare)
        yield " = "
        yield from self.expr().visit(node.value)
        yield ";"

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Iterable[str]:
        # if node.value is None:
        #     raise NotImplementedError(node, "empty value")
        yield from self.visit_lvalue(node.target, node.is_declare)
        if node.value:
            yield " = "
            yield from self.expr().visit(node.value)
        yield ";"


