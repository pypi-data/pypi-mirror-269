import abc
import ast
from dataclasses import dataclass, field
from typing import Optional, List

from transpiler.phases.typing.scope import Scope
from transpiler.phases.typing.types import BaseType, TY_NONE, TypeVariable, TY_TYPE, ResolvedConcreteType, TypeListType, \
    TY_BUILTIN_FEATURE, make_builtin_feature, TY_CPP_TYPE, make_cpp_type, GenericType, TY_UNION, ClassTypeType
from transpiler.phases.utils import NodeVisitorSeq


@dataclass
class TypeAnnotationVisitor(NodeVisitorSeq):
    scope: Scope

    def visit_str(self, node: str) -> BaseType:
        if existing := self.scope.get(node):
            ty = existing.type
            assert isinstance(ty, ResolvedConcreteType)
            assert ty.inherits(TY_TYPE)
            return ty.inner_type

        from transpiler.phases.typing.exceptions import UnknownNameError
        raise UnknownNameError(node)

    def visit_Name(self, node: ast.Name) -> BaseType:
        return self.visit_str(node.id)

    def visit_Constant(self, node: ast.Constant) -> BaseType:
        if node.value is None:
            return TY_NONE
        if type(node.value) == str:
            return node.value
        raise NotImplementedError

    def visit_Subscript(self, node: ast.Subscript) -> BaseType:
        ty_op = self.visit(node.value)
        args = list(node.slice.elts) if type(node.slice) == ast.Tuple else [node.slice]
        args = [self.visit(arg) for arg in args]
        if ty_op is TY_BUILTIN_FEATURE:
            assert len(args) == 1
            return make_builtin_feature(args[0])
        elif ty_op is TY_CPP_TYPE:
            assert len(args) == 1
            return make_cpp_type(args[0])
        assert isinstance(ty_op, GenericType)
        return ty_op.instantiate(args)

    def visit_Call(self, node: ast.Call) -> BaseType:
        if orig := getattr(node, "orig_node", None):
            if isinstance(orig, ast.Subscript):
                return self.visit_Subscript(orig)
        raise NotImplementedError()

    def visit_List(self, node: ast.List) -> BaseType:
        return TypeListType([self.visit(elt) for elt in node.elts])

    def visit_Attribute(self, node: ast.Attribute) -> BaseType:
        #raise NotImplementedError()
        from transpiler.phases.typing.expr import ScoperExprVisitor
        res = ScoperExprVisitor(self.scope).visit(node)
        assert isinstance(res, ClassTypeType)
        return res.inner_type

    def visit_BinOp(self, node: ast.BinOp) -> BaseType:
        if isinstance(node.op, ast.BitOr):
            return TY_UNION.instantiate([self.visit(node.left), self.visit(node.right)])
        raise NotImplementedError(node.op)
