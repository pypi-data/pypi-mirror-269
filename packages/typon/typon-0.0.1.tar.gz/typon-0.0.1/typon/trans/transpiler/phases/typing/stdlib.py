import ast
import copy
from dataclasses import dataclass, field
from logging import debug
from pathlib import Path
from typing import Optional, Callable

from transpiler.phases.typing.annotations import TypeAnnotationVisitor
from transpiler.phases.typing.common import PRELUDE, is_builtin
from transpiler.phases.typing.expr import ScoperExprVisitor
from transpiler.phases.typing.modules import parse_module
from transpiler.phases.typing.scope import Scope, VarDecl, VarKind, ScopeKind
from transpiler.phases.typing.types import BaseType, BuiltinGenericType, BuiltinType, create_builtin_generic_type, \
    create_builtin_type, ConcreteType, GenericInstanceType, TypeListType, TypeTupleType, GenericParameter, \
    GenericParameterKind, TypeVariable, ResolvedConcreteType, MemberDef, ClassTypeType, CallableInstanceType, \
    MethodType, GenericType, BlockData, TY_TASK, UserGenericType, UserType, BoundFuncTypeBase
from transpiler.phases.utils import NodeVisitorSeq
from transpiler.utils import highlight, linenodata


def visit_generic_item(
        visit_nongeneric: Callable[[Scope, ResolvedConcreteType], None],
        node,
        output_type: BuiltinGenericType,
        scope: Scope,
        instance_type=None,
        force_generic=False):
    if force_generic or node.type_params:
        output_type.parameters = []
        for param in node.type_params:
            match param:
                case ast.TypeVar(_, _):
                    kind = GenericParameterKind.NORMAL
                case ast.ParamSpec(_):
                    kind = GenericParameterKind.PARAMETERS
                case ast.TypeVarTuple(_):
                    kind = GenericParameterKind.TUPLE
            output_type.parameters.append(GenericParameter(param.name, kind))

        if instance_type is None:
            class instance_type(GenericInstanceType):
                pass

            instance_type.__name__ = f"GenericInstance${node.name}"

        def instantiate(args: list[ConcreteType]) -> GenericInstanceType:
            new_scope = scope.child(ScopeKind.GLOBAL)
            args_iter = iter(args)
            constraints = []
            anno = TypeAnnotationVisitor(new_scope)
            for param in node.type_params:
                op_val = next(args_iter, None)
                if op_val is None:
                    op_val = TypeVariable()
                match param:
                    case ast.TypeVar(name, bound):
                        new_scope.declare_local(name, op_val.type_type())
                        if bound is not None:
                            constraints.append((op_val, anno.visit(bound)))
                    case ast.ParamSpec(name):
                        assert isinstance(op_val, TypeListType)
                        new_scope.declare_local(name, op_val.type_type())
                    case ast.TypeVarTuple(name):
                        new_scope.declare_local(name, TypeTupleType(list(args_iter)).type_type())
            for a, b in constraints:
                assert b.try_assign(a)
            #  todo
            new_output_type = instance_type()
            new_output_type.generic_parent = output_type
            new_output_type.generic_args = args
            visit_nongeneric(new_scope, new_output_type)
            return new_output_type

        output_type.constraints_ = []
        output_type.instantiate_ = instantiate
    else:
        visit_nongeneric(scope, output_type)


@dataclass
class StdlibVisitor(NodeVisitorSeq):
    python_path: list[Path]
    scope: Scope = field(default_factory=lambda: PRELUDE)
    cur_class: Optional[ResolvedConcreteType] = None
    is_native: bool = False

    def resolve_module_import(self, name: str):
        # tries = [
        #     self.python_path.parent / f"{name}.py",
        #     self.python_path.parent / name
        # ]
        # for path in tries:
        #     if path.exists():
        #         return path
        # raise FileNotFoundError(f"Could not find module {name}")
        return parse_module(name, self.python_path, self.scope.child(ScopeKind.GLOBAL))

    def expr(self) -> ScoperExprVisitor:
        return ScoperExprVisitor(self.scope)

    def visit_Module(self, node: ast.Module):
        for stmt in node.body:
            self.visit(stmt)

    def visit_Assign(self, node: ast.Assign):
        if self.is_native:
            decl = VarDecl(VarKind.LOCAL, self.anno().visit(node.value).type_type())
        else:
            decl = VarDecl(VarKind.LOCAL, self.expr().visit(node.value), is_item_decl=True, from_node=node)
        self.scope.vars[node.targets[0].id] = decl

    def visit_AnnAssign(self, node: ast.AnnAssign):
        ty = self.anno().visit(node.annotation)
        if self.cur_class:
            assert isinstance(self.cur_class, ResolvedConcreteType)
            self.cur_class.fields[node.target.id] = MemberDef(ty, in_class_def=True, from_node=node)
        self.scope.vars[node.target.id] = VarDecl(VarKind.LOCAL, ty)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = self.resolve_module_import(node.module)
        node.module_obj = module
        for alias in node.names:
            thing = module.fields.get(alias.name)
            if not thing:
                from transpiler.phases.typing.exceptions import UnknownModuleMemberError
                raise UnknownModuleMemberError(node.module, alias.name)
            alias.item_obj = thing.type
            self.scope.vars[alias.asname or alias.name] = VarDecl(VarKind.LOCAL, thing.type)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            mod = self.resolve_module_import(alias.name)
            alias.module_obj = mod
            self.scope.vars[alias.asname or alias.name] = VarDecl(VarKind.LOCAL, mod)

    def visit_ClassDef(self, node: ast.ClassDef):
        force_generic = not self.is_native
        #force_generic = False
        if existing := self.scope.get(node.name):
            assert isinstance(existing.type, ClassTypeType)
            NewType = existing.type.inner_type
        else:
            if node.type_params or force_generic:
                base_class, base_type = create_builtin_generic_type, (
                    BuiltinGenericType if self.is_native else UserGenericType)
            else:
                base_class, base_type = create_builtin_type, (BuiltinType if self.is_native else UserType)
            NewType = base_class(node.name,
                                 "Builtin" if self.is_native else "User",
                                 base_type
                                 )
            self.scope.vars[node.name] = VarDecl(VarKind.LOCAL, NewType.type_type(), is_item_decl=True)

        def visit_nongeneric(scope: Scope, output: ResolvedConcreteType):
            cl_scope = scope.child(ScopeKind.CLASS)
            cl_scope.declare_local("Self", output.type_type())
            output.block_data = BlockData(copy.deepcopy(node), scope)
            visitor = StdlibVisitor(self.python_path, cl_scope, output, self.is_native)
            bases = [self.anno().visit(base) for base in node.bases]
            match bases:
                case []:
                    pass
                case [prot] if is_builtin(prot, "Protocol"):
                    output.is_protocol = True
                case _:
                    output.parents = [p.deref() for p in bases]  # TODO: what about uninstantiated generic types here?
            for stmt in node.body:
                visitor.visit(stmt)
            for deco_node in node.decorator_list:
                deco = self.expr().visit(deco_node)
                match deco:
                    case dc if is_builtin(dc, "dataclass"):
                        real_fields = {k: m for k, m in output.fields.items() if
                                       not isinstance(m.from_node, ast.FunctionDef)}
                        generated_init = ast.FunctionDef(
                            name="__init__",
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[ast.arg(arg="self", annotation=None)] +
                                     [ast.arg(arg=k, annotation=None) for k, m in real_fields.items()],
                                vararg=None, kwonlyargs=[],
                                kw_defaults=[], kwarg=None,
                                defaults=[]), body=[
                                ast.Assign(
                                    targets=[
                                        ast.Attribute(value=ast.Name("self", ast.Load()), attr=k, ctx=ast.Store())
                                    ],
                                    value=ast.Name(k, ast.Load()),
                                    type_comment=None,
                                    **linenodata(node)
                                ) for k in real_fields],
                            decorator_list=[],
                            returns=None,
                            type_params=[],
                            **linenodata(node))
                        visitor.visit(generated_init)
                    case _:
                        raise NotImplementedError(f"Decorator {deco} not handled yet")
            if "__init__" not in output.fields:
                visitor.visit(ast.FunctionDef(
                    name="__init__",
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[ast.arg(arg="self", annotation=None)],
                        vararg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=None,
                        defaults=[]
                    ),
                    body=[ast.Pass()],
                    decorator_list=[],
                    returns=None,
                    type_params=[],
                    **linenodata(node)
                ))

        visit_generic_item(visit_nongeneric, node, NewType, self.scope, force_generic=force_generic)

    def visit_Pass(self, node: ast.Pass):
        pass

    def visit_FunctionDef(self, node: ast.FunctionDef):
        def visit_nongeneric(scope, output: CallableInstanceType):
            scope = scope.child(ScopeKind.FUNCTION)
            scope.function = scope
            scope.obj_type = output
            arg_visitor = TypeAnnotationVisitor(scope)
            output.block_data = BlockData(copy.deepcopy(node), scope)
            output.parameters = [arg_visitor.visit(arg.annotation) for arg in node.args.args]
            for arg, ty in zip(node.args.args, output.parameters):
                scope.declare_local(arg.arg, ty)
            output.return_type = arg_visitor.visit(node.returns)
            output.optional_at = len(node.args.args) - len(node.args.defaults)
            output.is_variadic = args.vararg is not None
            output.is_native = self.is_native
            if not self.is_native:
                output.return_type = TY_TASK.instantiate([output.return_type])

        @dataclass(eq=False, init=False)
        class InstanceType(CallableInstanceType):
            def __init__(self, **kwargs):
                super().__init__(**{"parameters": None, "return_type": None, **kwargs})

            def __str__(self):
                return f"{node.name}{super().__str__()}"

        args = node.args
        assert args.posonlyargs == []
        assert args.kwonlyargs == []
        assert args.kw_defaults == []
        assert args.kwarg is None

        for i, arg in enumerate(args.args):
            arg: ast.arg
            """ arg(identifier arg, expr? annotation, string? type_comment) """
            if arg.annotation is None:
                if i == 0 and self.cur_class is not None:
                    arg_name = "Self"
                else:
                    arg_name = f"AutoVar${abs(hash(arg.arg))}"
                node.type_params.append(ast.TypeVar(arg_name, None))  # todo: bounds
                arg.annotation = ast.Name(arg_name, ast.Load())
            else:
                if isinstance(arg.annotation, ast.Name) and (
                        # arg.annotation.id == "Self" or
                        any(k.name == arg.annotation.id for k in node.type_params)
                ):
                    # annotation is type variable so we keep it
                    pass
                else:
                    arg_name = f"AutoBoundedVar${abs(hash(arg.arg))}"
                    node.type_params.append(ast.TypeVar(arg_name, arg.annotation))
                    arg.annotation = ast.Name(arg_name, ast.Load())

        if node.returns is None:
            node.returns = ast.Name("AutoVar$return", ast.Load())
            node.type_params.append(ast.TypeVar("AutoVar$return", None))

        # if self.cur_class is not None:
        #     node.type_params.append(ast.TypeVar("Self", None))

        if True or node.type_params:
            bases = [BuiltinGenericType]
            cur_class_ref = self.cur_class
            if cur_class_ref is not None:
                bases.append(MethodType)

            class FuncType(*bases):
                def name(self):
                    return f"FuncTypeGen${node.name}"

                if cur_class_ref is not None:
                    def remove_self(self, self_type):
                        class BoundFuncType(BoundFuncTypeBase, GenericType):
                            def name(self) -> str:
                                return f"BoundFuncType${node.name}"

                            def _instantiate(self, args: list[ConcreteType]) -> GenericInstanceType:
                                return NewType.instantiate(args).remove_self(self_type)

                            def __str__(self):
                                return str(self.instantiate_default())

                        res = BoundFuncType()
                        res.parameters = NewType.parameters
                        return res
        else:
            class FuncType(InstanceType):
                pass
        base_class = FuncType
        NewType = base_class()
        FuncType.__name__ = NewType.name()

        for deco_node in copy.deepcopy(node.decorator_list):
            if isinstance(deco_node, ast.Call):
                deco_args = deco_node.args
                deco_node = deco_node.func
            else:
                deco_args = []
            deco = self.expr().visit(deco_node)
            match deco:
                case dc if is_builtin(dc, "PybindExport"):
                    assert len(deco_args) == 1
                    export = deco_args[0]
                    assert isinstance(export, ast.List)
                    exports = [self.anno().visit(e) for e in export.elts]
                    NewType.pybind_exports = exports
                case _:
                    raise NotImplementedError(f"Decorator {deco} not handled yet")

        self.scope.vars[node.name] = VarDecl(VarKind.LOCAL, NewType, is_item_decl=True, from_node=node)
        if self.cur_class is not None:
            self.cur_class.fields[node.name] = MemberDef(NewType, node, in_class_def=True, from_node=node)

        visit_generic_item(visit_nongeneric, node, NewType, self.scope, InstanceType, True)

    def visit_Assert(self, node: ast.Assert):
        if isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not):
            oper = node.test.operand
            try:
                res = self.expr().visit(oper)
            except:
                debug(f"Type of {ast.unparse(oper)} := INVALID")
            else:
                raise AssertionError(f"Assertion should fail, got {res} for {ast.unparse(oper)}")
        else:
            debug(f"Type of {highlight(ast.unparse(node.test))} := {highlight(self.expr().visit(node.test))}")

    def anno(self) -> "TypeAnnotationVisitor":
        return TypeAnnotationVisitor(self.scope)

    def visit_str(self, node: str) -> BaseType:
        if existing := self.scope.get(node):
            return existing.type
        from transpiler.phases.typing.exceptions import UnknownNameError
        raise UnknownNameError(node)

    def visit_Name(self, node: ast.Name) -> BaseType:
        return self.visit_str(node.id)
