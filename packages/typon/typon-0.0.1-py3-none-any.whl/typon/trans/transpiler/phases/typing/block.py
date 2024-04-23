import ast
import copy
import dataclasses
import importlib
from dataclasses import dataclass

from transpiler.exceptions import CompileError
from transpiler.phases.typing.types import BaseType, TypeVariable, CallableInstanceType, TY_NONE, \
    TupleInstanceType, RuntimeValue, PromiseKind, GenericInstanceType, TRANSPARENT_PROMISES, PROMISES
from transpiler.utils import highlight, linenodata
from transpiler.phases.typing.common import ScoperVisitor, is_builtin, DeclareInfo
from transpiler.phases.typing.expr import ScoperExprVisitor, DUNDER
from transpiler.phases.typing.scope import VarDecl, VarKind, ScopeKind, Scope
from transpiler.phases.utils import PlainBlock, AnnotationName


@dataclass
class ScoperBlockVisitor(ScoperVisitor):
    stdlib: bool = False

    def visit_Pass(self, node: ast.Pass):
        pass

    # def get_module(self, name: str) -> VarDecl:
    #     mod = self.scope.get(name, VarKind.MODULE)
    #     if mod is None:
    #         # try lookup with importlib
    #         py_mod = importlib.import_module(name)
    #         mod_scope = Scope()
    #         # copy all functions to mod_scope
    #         for fname, obj in py_mod.__dict__.items():
    #             if callable(obj):
    #                 # fty = FunctionType([], TypeVariable())
    #                 # fty.is_python_func = True
    #                 fty = TypeVariable()
    #                 fty.is_python_func = True
    #                 mod_scope.vars[fname] = VarDecl(VarKind.LOCAL, fty)
    #         mod = make_mod_decl(name, mod_scope)
    #         mod.type.is_python = True
    #         self.scope.vars[name] = mod
    #     if mod is None:
    #         from transpiler.phases.typing.exceptions import UnknownNameError
    #         raise UnknownNameError(name)
    #     assert isinstance(mod, VarDecl), mod
    #     assert isinstance(mod.type, ModuleType), mod.type
    #     return mod
    #
    # def visit_Import(self, node: ast.Import):
    #     for alias in node.names:
    #         mod = self.get_module(alias.name)
    #         alias.module_obj = mod.type
    #         self.scope.vars[alias.asname or alias.name] = dataclasses.replace(mod, kind=VarKind.LOCAL)
    #
    # def visit_ImportFrom(self, node: ast.ImportFrom):
    #     if node.module in {"typing2", "__future__"}:
    #         return
    #     module = self.get_module(node.module)
    #     node.module_obj = module.type
    #     for alias in node.names:
    #         thing = module.val.get(alias.name)
    #         if not thing:
    #             from transpiler.phases.typing.exceptions import UnknownModuleMemberError
    #             raise UnknownModuleMemberError(node.module, alias.name)
    #         alias.item_obj = thing
    #         self.scope.vars[alias.asname or alias.name] = VarDecl(VarKind.LOCAL, thing)
    #
    # def visit_Module(self, node: ast.Module):
    #     self.visit_block(node.body)

    def get_type(self, node: ast.expr) -> BaseType:
        if type := getattr(node, "type", None):
            return type
        self.expr().visit(node)
        return node.type
        # ntype = TypeVariable()
        # node.type = ntype
        # return ntype

    def visit_Assign(self, node: ast.Assign):
        if len(node.targets) != 1:
            raise NotImplementedError(node)
        target = node.targets[0]
        ty = self.get_type(node.value)
        decl = self.visit_assign_target(target, ty, node.value)
        node.is_declare = DeclareInfo(decl, node.value) if decl else None

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if node.simple != 1:
            raise NotImplementedError(node)
        if not isinstance(node.target, ast.Name):
            raise NotImplementedError(node)
        ty = self.visit_annotation(node.annotation)
        decl = self.visit_assign_target(node.target, ty, node.value)
        node.is_declare = DeclareInfo(decl, node.value) if decl else None
        if node.value is not None:
            ty_val = self.get_type(node.value)
            __TB__ = f"unifying annotation {highlight(node.annotation)} with value {highlight(node.value)} of type {highlight(ty_val)}"
            ty.unify(ty_val)

    def visit_assign_target(self, target, decl_val: BaseType, val: ast.expr = None) -> bool:
        __TB__ = f"analyzing assignment target {highlight(target)} with value {highlight(decl_val)}"
        if isinstance(target, ast.Name):
            if target.id == "_":
                return False
            target.type = decl_val
            if vdecl := self.scope.get(target.id, {VarKind.LOCAL, VarKind.GLOBAL, VarKind.NONLOCAL}, restrict_function=True):
                __TB__ = f"unifying existing variable {highlight(target.id)} of type {highlight(vdecl.type)} with assigned value {highlight(decl_val)}"
                vdecl.type.unify(decl_val)
                return False
            else:
                # self.scope.vars[target.id] = VarDecl(VarKind.LOCAL, decl_val)
                # if self.scope.kind == ScopeKind.FUNCTION_INNER:
                #     self.root_decls[target.id] = VarDecl(VarKind.OUTER_DECL, decl_val)
                #     return False
                # return True
                val = val or RuntimeValue()
                self.scope.function.vars[target.id] = VarDecl(VarKind.LOCAL, decl_val, val)
                #if self.scope.kind == ScopeKind.FUNCTION_INNER:
                #if not isinstance(val, RuntimeValue):
                if True:
                    self.scope.function.root_decls[target.id] = val if not isinstance(val, RuntimeValue) else decl_val
                    return False
                return True
        elif isinstance(target, ast.Tuple):
            if not isinstance(decl_val, TupleInstanceType):
                from transpiler.phases.typing.exceptions import InvalidUnpackError
                raise InvalidUnpackError(decl_val)
            if len(target.elts) != len(decl_val.fields):
                from transpiler.phases.typing.exceptions import InvalidUnpackCountError
                raise InvalidUnpackCountError(decl_val, len(target.elts))
            target.type = decl_val
            decls = [self.visit_assign_target(t, ty, ast.Name(str(t))) for t, ty in zip(target.elts, decl_val.fields)]  # eager evaluated
            return decls
        elif isinstance(target, ast.Attribute):
            attr_type = self.expr().visit(target)
            attr_type.unify(decl_val)
            return False
        elif isinstance(target, ast.Subscript):
            expr = self.expr()
            left = expr.visit(target.value)
            args = target.slice if type(target.slice) == tuple else [target.slice]
            args = [expr.visit(e) for e in args]
            if len(args) == 1:
                args = args[0]
            expr.make_dunder([left, args, decl_val], "setitem")
            target.type = TypeVariable()
            target.type.unify(decl_val)
            return False
        else:
            raise NotImplementedError(ast.unparse(target))

    def visit_If(self, node: ast.If):
        scope = self.scope.child(ScopeKind.FUNCTION_INNER)
        node.inner_scope = scope
        self.expr().visit(node.test)
        then_scope = scope.child(ScopeKind.FUNCTION_INNER)
        then_visitor = ScoperBlockVisitor(then_scope, self.root_decls)
        then_visitor.visit_block(node.body)
        if node.orelse:
            else_scope = scope.child(ScopeKind.FUNCTION_INNER)
            else_visitor = ScoperBlockVisitor(else_scope, self.root_decls)
            else_visitor.visit_block(node.orelse)
            node.orelse_scope = else_scope
            if then_scope.diverges and else_scope.diverges:
                self.scope.diverges = True

    def visit_While(self, node: ast.While):
        scope = self.scope.child(ScopeKind.FUNCTION_INNER)
        scope.is_loop = node
        node.inner_scope = scope
        self.expr().visit(node.test)
        body_scope = scope.child(ScopeKind.FUNCTION_INNER)
        body_visitor = ScoperBlockVisitor(body_scope, self.root_decls)
        body_visitor.visit_block(node.body)
        if node.orelse:
            orelse_scope = scope.child(ScopeKind.FUNCTION_INNER)
            orelse_visitor = ScoperBlockVisitor(orelse_scope, self.root_decls)
            orelse_visitor.visit_block(node.orelse)
            node.orelse_variable = f"orelse_{id(node)}"

    def visit_PlainBlock(self, node: PlainBlock):
        scope = self.scope.child(ScopeKind.FUNCTION_INNER)
        node.inner_scope = scope
        body_visitor = ScoperBlockVisitor(scope, self.root_decls)
        body_visitor.visit_block(node.body)

    def visit_For(self, node: ast.For):
        scope = self.scope.child(ScopeKind.FUNCTION_INNER)
        scope.is_loop = node
        node.inner_scope = scope
        assert isinstance(node.target, ast.Name)
        var_var = TypeVariable()
        scope.vars[node.target.id] = VarDecl(VarKind.LOCAL, var_var)
        seq_type = self.expr().visit(node.iter)
        iter_type = self.get_iter(seq_type)
        next_type = self.get_next(iter_type)
        var_var.unify(next_type)
        body_scope = scope.child(ScopeKind.FUNCTION_INNER)
        body_visitor = ScoperBlockVisitor(body_scope, self.root_decls)
        body_visitor.visit_block(node.body)
        if node.orelse:
            orelse_scope = scope.child(ScopeKind.FUNCTION_INNER)
            orelse_visitor = ScoperBlockVisitor(orelse_scope, self.root_decls)
            orelse_visitor.visit_block(node.orelse)
            node.orelse_variable = f"orelse_{id(node)}"

    def visit_Expr(self, node: ast.Expr):
        self.expr().visit(node.value)

    def visit_Return(self, node: ast.Return):
        fct = self.scope.function
        if fct is None:
            from transpiler.phases.typing.exceptions import OutsideFunctionError
            raise OutsideFunctionError()
        ftype = fct.obj_type
        assert isinstance(ftype, CallableInstanceType)
        vtype = self.expr().visit(node.value) if node.value else TY_NONE

        ret = ftype.return_type.resolve()
        if isinstance(ret, GenericInstanceType) and ret.generic_parent in PROMISES:
            ret = ret.generic_args[0]
        vtype.unify(ret)
        self.scope.diverges = True
        fct.has_return = True

    def visit_Global(self, node: ast.Global):
        for name in node.names:
            self.scope.function.vars[name] = VarDecl(VarKind.GLOBAL, None)
            if name not in self.scope.global_scope.vars:
                self.scope.global_scope.vars[name] = VarDecl(VarKind.LOCAL, None)

    def visit_Nonlocal(self, node: ast.Global):
        fct = self.scope.function
        if fct is None:
            from transpiler.phases.typing.exceptions import OutsideFunctionError
            raise OutsideFunctionError()
        for name in node.names:
            fct.vars[name] = VarDecl(VarKind.NONLOCAL, None)
            if name not in fct.parent.vars:
                fct.parent.vars[name] = VarDecl(VarKind.LOCAL, None)

    def visit_AugAssign(self, node: ast.AugAssign):
        target, value = map(self.get_type, (node.target, node.value))
        try:
            self.expr().make_dunder([target, value], "i" + DUNDER[type(node.op)])
        except CompileError as e:
            self.visit_assign_target(node.target, self.expr().make_dunder([target, value], DUNDER[type(node.op)]))
            # equivalent = ast.Assign(
            #     targets=[node.target],
            #     value=ast.BinOp(left=node.target, op=node.op, right=node.value, **linenodata(node)),
            #     **linenodata(node))
            # self.visit(equivalent)

    def visit(self, node: ast.AST):
        if isinstance(node, ast.AST):
            __TB_SKIP__ = True
            super().visit(node)
            node.scope = self.scope
        else:
            raise NotImplementedError(node)

    def visit_Break(self, _node: ast.Break):
        if not self.scope.is_in_loop():
            from transpiler.phases.typing.exceptions import OutsideLoopError
            raise OutsideLoopError()

    def visit_Continue(self, _node: ast.Continue):
        if not self.scope.is_in_loop():
            from transpiler.phases.typing.exceptions import OutsideLoopError
            raise OutsideLoopError()

    def visit_Try(self, node: ast.Try):
        scope = self.scope.child(ScopeKind.FUNCTION_INNER)
        node.inner_scope = scope
        body_scope = scope.child(ScopeKind.FUNCTION_INNER)
        body_visitor = ScoperBlockVisitor(body_scope, self.root_decls)
        body_visitor.visit_block(node.body)
        # todo
        for handler in node.handlers:
            handler_scope = scope.child(ScopeKind.FUNCTION_INNER)
            handler_visitor = ScoperBlockVisitor(handler_scope, self.root_decls)
            handler_visitor.visit_block(handler.body)
        if node.orelse:
            else_scope = scope.child(ScopeKind.FUNCTION_INNER)
            else_visitor = ScoperBlockVisitor(else_scope, self.root_decls)
            else_visitor.visit_block(node.orelse)
        if node.finalbody:
            raise NotImplementedError(node.finalbody)

    def visit_Raise(self, node: ast.Raise):
        self.scope.diverges = True
        if node.exc:
            self.expr().visit(node.exc)
        if node.cause:
            self.expr().visit(node.cause)