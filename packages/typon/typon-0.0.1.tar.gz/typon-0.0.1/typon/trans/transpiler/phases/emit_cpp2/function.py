# coding: utf-8
import ast
from dataclasses import dataclass
from typing import Iterable

from transpiler.phases.emit_cpp.consts import SYMBOLS
from transpiler.phases.emit_cpp import CoroutineMode, FunctionEmissionKind
from transpiler.phases.emit_cpp.block import BlockVisitor
from transpiler.phases.typing.scope import Scope
from transpiler.phases.utils import PlainBlock


# noinspection PyPep8Naming
@dataclass
class FunctionVisitor(BlockVisitor):
    def visit_Expr(self, node: ast.Expr) -> Iterable[str]:
        yield from self.expr().visit(node.value)
        yield ";"

    def visit_AugAssign(self, node: ast.AugAssign) -> Iterable[str]:
        yield from self.visit_lvalue(node.target, False)
        yield SYMBOLS[type(node.op)] + "="
        yield from self.expr().visit(node.value)
        yield ";"

    def visit_For(self, node: ast.For) -> Iterable[str]:
        if not isinstance(node.target, ast.Name):
            raise NotImplementedError(node)
        if node.orelse:
            yield "auto"
            yield node.orelse_variable
            yield "= true;"
        yield f"for (auto {node.target.id} : "
        yield from self.expr().visit(node.iter)
        yield ")"
        yield from self.emit_block(node.inner_scope, node.body) # TODO: why not reuse the scope used for analysis? same in while
        if node.orelse:
            yield "if ("
            yield node.orelse_variable
            yield ")"
            yield from self.emit_block(node.inner_scope, node.orelse)

    def visit_If(self, node: ast.If) -> Iterable[str]:
        yield "if ("
        yield from self.expr().visit(node.test)
        yield ")"
        yield from self.emit_block(node.inner_scope, node.body)
        if node.orelse:
            yield "else "
            if isinstance(node.orelse, ast.If):
                yield from self.visit(node.orelse)
            else:
                yield from self.emit_block(node.orelse_scope, node.orelse)

    def visit_PlainBlock(self, node: PlainBlock) -> Iterable[str]:
        yield from self.emit_block(node.inner_scope, node.body)

    def visit_Return(self, node: ast.Return) -> Iterable[str]:
        if CoroutineMode.ASYNC in self.generator:
            yield "co_return "
        else:
            yield "return "
        if node.value:
            yield from self.expr().visit(node.value)
        yield ";"

    def visit_While(self, node: ast.While) -> Iterable[str]:
        if node.orelse:
            yield "auto"
            yield node.orelse_variable
            yield "= true;"
        yield "while ("
        yield from self.expr().visit(node.test)
        yield ")"
        yield from self.emit_block(node.inner_scope, node.body)
        if node.orelse:
            yield "if ("
            yield node.orelse_variable
            yield ")"
            yield from self.emit_block(node.inner_scope, node.orelse)

    def visit_Global(self, node: ast.Global) -> Iterable[str]:
        yield ""

    def visit_Nonlocal(self, node: ast.Nonlocal) -> Iterable[str]:
        yield ""

    def block2(self) -> "FunctionVisitor":
        # See the comments in visit_FunctionDef.
        # A Python code block does not introduce a new scope, so we create a new `Scope` object that shares the same
        # variables as the parent scope.
        return FunctionVisitor(self.scope.child_share(), generator=self.generator)

    def emit_block(self, scope: Scope, items: Iterable[ast.stmt]) -> Iterable[str]:
        yield "{"
        for child in items:
            yield from FunctionVisitor(scope, generator=self.generator).visit(child)
        yield "}"

    def visit_Break(self, node: ast.Break) -> Iterable[str]:
        if (loop := self.scope.is_in_loop()).orelse:
            yield loop.orelse_variable
            yield " = false;"
        yield "break;"

    def visit_Try(self, node: ast.Try) -> Iterable[str]:
        yield from self.emit_block(node.inner_scope, node.body)
        if node.orelse:
            raise NotImplementedError(node, "orelse")
        if node.finalbody:
            raise NotImplementedError(node, "finalbody")
        for handler in node.handlers:
            #yield from self.visit(handler)
            pass
            # todo

    def visit_Raise(self, node: ast.Raise) -> Iterable[str]:
        yield "// raise"
        # TODO

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
        yield "auto"
        yield self.fix_name(node.name)
        yield "="
        yield from self.visit_func_new(node, FunctionEmissionKind.LAMBDA)
        yield ";"
