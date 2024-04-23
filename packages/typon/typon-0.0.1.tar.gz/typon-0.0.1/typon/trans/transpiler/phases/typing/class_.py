# coding: utf-8
# import ast
# from dataclasses import dataclass, field
#
# from transpiler.phases.typing import FunctionType, ScopeKind, VarDecl, VarKind, TY_NONE
# from transpiler.phases.typing.common import ScoperVisitor
# from transpiler.phases.typing.types import PromiseKind, Promise, BaseType, MemberDef
#
#
# @dataclass
# class ScoperClassVisitor(ScoperVisitor):
#     fdecls: list[(ast.FunctionDef, BaseType)] = field(default_factory=list)
#
#     def visit_AnnAssign(self, node: ast.AnnAssign):
#         assert node.value is None, "Class field should not have a value"
#         assert node.simple == 1, "Class field should be simple (identifier, not parenthesized)"
#         assert isinstance(node.target, ast.Name)
#         self.scope.obj_type.fields[node.target.id] = MemberDef(self.visit_annotation(node.annotation))
#
#     def visit_Assign(self, node: ast.Assign):
#         assert len(node.targets) == 1, "Can't use destructuring in class static member"
#         assert isinstance(node.targets[0], ast.Name)
#         node.is_declare = True
#         valtype = self.expr().visit(node.value)
#         node.targets[0].type = valtype
#         self.scope.obj_type.fields[node.targets[0].id] = MemberDef(valtype, node.value)
#
#     def visit_FunctionDef(self, node: ast.FunctionDef):
#         ftype = self.parse_function(node)
#         ftype.parameters[0].unify(self.scope.obj_type)
#         inner = ftype.return_type
#         if node.name != "__init__":
#             ftype.return_type = Promise(ftype.return_type, PromiseKind.TASK)
#         ftype.is_method = True
#         self.scope.obj_type.fields[node.name] = MemberDef(ftype, node)
#         return (node, inner)
