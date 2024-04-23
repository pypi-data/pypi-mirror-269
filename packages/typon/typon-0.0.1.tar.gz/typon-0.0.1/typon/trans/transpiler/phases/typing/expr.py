import abc
import ast
import inspect
from itertools import zip_longest
from typing import List

from transpiler.phases.typing.common import ScoperVisitor, is_builtin
from transpiler.phases.typing.exceptions import ArgumentCountMismatchError, TypeMismatchKind, TypeMismatchError
from transpiler.phases.typing.types import BaseType, TY_STR, TY_BOOL, TY_INT, TY_COMPLEX, TY_FLOAT, TY_NONE, \
    ClassTypeType, ResolvedConcreteType, GenericType, CallableInstanceType, TY_LIST, TY_SET, TY_DICT, RuntimeValue, \
    TypeVariable, TY_LAMBDA, TypeListType, MethodType, TY_TUPLE, GenericInstanceType, PROMISES, TRANSPARENT_PROMISES, \
    TY_FORKED, TY_JOIN, TypeTupleType, TupleInstanceType, TY_TYPE, TY_SLICE, BoundFuncTypeBase
from transpiler.phases.typing.scope import ScopeKind, VarDecl, VarKind
from transpiler.utils import linenodata

DUNDER = {
    ast.Eq: "eq",
    ast.NotEq: "ne",
    ast.Mult: "mul",
    ast.Add: "add",
    ast.Sub: "sub",
    ast.Div: "truediv",
    ast.FloorDiv: "floordiv",
    ast.Mod: "mod",
    ast.Lt: "lt",
    ast.Gt: "gt",
    ast.GtE: "ge",
    ast.LtE: "le",
    ast.LShift: "lshift",
    ast.RShift: "rshift",
    ast.BitXor: "xor",
    ast.BitOr: "or",
    ast.BitAnd: "and",
    ast.USub: "neg",
    ast.UAdd: "pos",
    ast.Invert: "invert",
    ast.In: "contains",
}

class ScoperExprVisitor(ScoperVisitor):
    def visit(self, node):
        res = self.visit_inner(node)
        if self.scope.function and isinstance(res, GenericInstanceType) and res.generic_parent is TY_FORKED:
            fty = self.scope.function.obj_type.return_type
            if fty.generic_parent in PROMISES:
                fty = fty.generic_args[0] # todo: check if this whole if-block works
            self.scope.function.obj_type.return_type = TY_JOIN.instantiate([fty])

        return res

    def visit_inner(self, node) -> BaseType:
        if existing := getattr(node, "type", None):
            return existing.resolve()
        __TB_SKIP__ = True
        res = super().visit(node)
        if not res:
            __TB_SKIP__ = False
            raise NotImplementedError(f"`{ast.unparse(node)}` {type(node)}")
        res = res.resolve()
        if True or not hasattr(res, "from_node"):
            res.from_node = node
        node.type = res
        if orig := getattr(node, "orig_node", None):
            orig.type = res
        return res

    def visit_Tuple(self, node: ast.Tuple) -> BaseType:
        return TY_TUPLE.instantiate([self.visit(e) for e in node.elts])

    def visit_Slice(self, node: ast.Slice) -> BaseType:
        for n in ("lower", "upper", "step"):
            if arg := getattr(node, n):
                self.visit(arg).unify(TY_INT)
        return TY_SLICE


    def visit_Yield(self, node: ast.Yield) -> BaseType:
        ytype = self.visit(node.value)

        ftype = self.scope.function.obj_type.return_type
        assert isinstance(ftype, Promise)
        assert ftype.kind == PromiseKind.TASK
        ftype.kind = PromiseKind.GENERATOR
        ftype.return_type.unify(ytype)
        self.scope.function.has_yield = True

        return TY_NONE

    def visit_Constant(self, node: ast.Constant) -> BaseType:
        if isinstance(node.value, str):
            return TY_STR
        elif isinstance(node.value, bool):
            return TY_BOOL
        elif isinstance(node.value, int):
            return TY_INT
        elif isinstance(node.value, complex):
            return TY_COMPLEX
        elif isinstance(node.value, float):
            return TY_FLOAT
        elif node.value is None:
            return TY_NONE
        else:
            raise NotImplementedError(node, type(node))

    def visit_Name(self, node: ast.Name) -> BaseType:
        obj = self.scope.get(node.id)
        if not obj:
            from transpiler.phases.typing.exceptions import UnknownNameError
            raise UnknownNameError(node.id)
        ty = obj.type.resolve()
        # if isinstance(ty, TypeType) and isinstance(ty.type_object, TypeVariable):
        #     raise NameError(f"Use of type variable")  # todo: when does this happen exactly?
        # if getattr(ty, "is_python_func", False):
        #     ty.python_func_used = True
        return ty

    def visit_BoolOp(self, node: ast.BoolOp) -> BaseType:
        for value in node.values:
            self.visit(value)
        return TY_BOOL

    def visit_Call(self, node: ast.Call) -> BaseType:
        if orig := getattr(node, "orig_node", None):
            if isinstance(orig, ast.Subscript):
                left = self.visit(orig.value)
                if isinstance(left, TupleInstanceType):
                    if not (isinstance(orig.slice, ast.Constant) and isinstance(orig.slice.value, int)):
                        raise NotImplementedError("Tuple subscript with non-constant not handled yet")
                    return left.fields[orig.slice.value]
        ftype = self.visit(node.func)
        from transpiler.exceptions import CompileError
        rtype = self.visit_function_call(ftype, [self.visit(arg) for arg in node.args])
        actual = rtype
        node.is_await = False
        if isinstance(actual, GenericInstanceType) and actual.generic_parent in PROMISES:
            node.is_await = True
            if actual.generic_parent in TRANSPARENT_PROMISES:
                actual = actual.generic_args[0].resolve()

        return actual

    def visit_function_call(self, ftype: ResolvedConcreteType, arguments: List[BaseType]):
        ftype = ftype.deref()
        if isinstance(ftype, ClassTypeType):
            ftype = ftype.inner_type.deref()
            init = self.visit_getattr(TY_TYPE.instantiate([ftype]), "__init__")
            self.visit_function_call(init, [ftype, *arguments])
            return ftype

        # assert isinstance(ftype, CallableInstanceType) TODO

        if isinstance(ftype, TypeVariable) and ftype.python_func_placeholder:
            ret = TypeVariable()
            new_ftype = CallableInstanceType(arguments, ret)
            new_ftype.is_native = True
            ftype.unify(new_ftype)
            return ret

        if not isinstance(ftype, CallableInstanceType):
            return TypeVariable()

        for i, (a, b) in enumerate(zip_longest(ftype.parameters, arguments)):
            if b is None:
                if i >= ftype.optional_at:
                    continue
                raise ArgumentCountMismatchError(ftype, arguments)
            if a is None:
                if ftype.is_variadic:
                    break
                raise ArgumentCountMismatchError(ftype, arguments)
            if not a.try_assign(b):
                a.try_assign(b)
                raise TypeMismatchError(a, b, TypeMismatchKind.DIFFERENT_TYPE)

            if not ftype.is_native:
                if isinstance(ftype.generic_parent, BoundFuncTypeBase):
                    i += 1
                pname = ftype.block_data.node.args.args[i].arg
                ftype.block_data.scope.declare_local(pname, b)

        if not ftype.is_native:
            existing = ftype.generic_parent.find_cached_instance(ftype.generic_args)
            if not existing:
                ftype.generic_parent.cache_instance(ftype.generic_args, ftype)
                from transpiler.phases.typing.block import ScoperBlockVisitor
                scope = ftype.block_data.scope
                vis = ScoperBlockVisitor(scope)
                for stmt in ftype.block_data.node.body:
                    vis.visit(stmt)
                if not getattr(scope.function, "has_return", False):
                    stmt = ast.Return()
                    ftype.block_data.node.body.append(stmt)
                    vis.visit(stmt)
            else:
                return existing.return_type.resolve()
        return ftype.return_type.resolve()
        # if isinstance(ftype, TypeType):# and isinstance(ftype.type_object, UserType):
        #     init: FunctionType = self.visit_getattr(ftype, "__init__").remove_self()
        #     init.return_type = ftype.type_object
        #     return self.visit_function_call(init, arguments)
        # if isinstance(ftype, FunctionType):
        #     ret = ftype.return_type
        # elif isinstance(ftype, TypeVariable):
        #     ret = TypeVariable()
        # else:
        #     from transpiler.phases.typing.exceptions import NotCallableError
        #     raise NotCallableError(ftype)
        # #is_generic = any(isinstance(arg, TypeVariable) for arg in ftype.to_list())
        # equivalent = FunctionType(arguments, ret)
        # equivalent.is_intermediary = True
        # ftype.unify(equivalent)
        # return equivalent.return_type

    def visit_Lambda(self, node: ast.Lambda) -> BaseType:
        argtypes = [TypeVariable(decltype_str=f"decltype({arg.arg})") for arg in node.args.args]
        rtype = TypeVariable()
        ftype = TY_LAMBDA.instantiate([TypeListType(argtypes), rtype])
        scope = self.scope.child(ScopeKind.FUNCTION)
        scope.obj_type = ftype
        scope.function = scope
        node.inner_scope = scope
        node.body.scope = scope
        for arg, ty in zip(node.args.args, argtypes):
            scope.vars[arg.arg] = VarDecl(VarKind.LOCAL, ty)
        decls = {}
        visitor = ScoperExprVisitor(scope, decls)
        rtype.unify(visitor.visit(node.body))
        node.body.decls = decls
        return ftype

    def visit_BinOp(self, node: ast.BinOp) -> BaseType:
        left, right = map(self.visit, (node.left, node.right))
        return TypeVariable() # TODO

    # def visit_BinOp(self, node: ast.BinOp) -> BaseType:
    #     left, right = map(self.visit, (node.left, node.right))
    #     return self.make_dunder([left, right], DUNDER[type(node.op)])

    # def visit_Compare(self, node: ast.Compare) -> BaseType:
    #     left, right = map(self.visit, (node.left, node.comparators[0]))
    #     op = node.ops[0]
    #     if type(op) == ast.In:
    #         left, right = right, left
    #     return self.make_dunder([left, right], DUNDER[type(op)])

    def visit_Attribute(self, node: ast.Attribute) -> BaseType:
        ltype = self.visit(node.value)
        return self.visit_getattr(ltype, node.attr)

    def visit_getattr(self, ltype: BaseType, name: str) -> BaseType:

        bound = True
        if isinstance(ltype, ClassTypeType):
            # if mdecl := ltype.static_members.get(name):
            #     attr = mdecl.type
            #     if getattr(attr, "is_python_func", False):
            #         attr.python_func_used = True
            #     return attr
            ltype = ltype.inner_type
            bound = False

        ltype = ltype.deref()

        #assert isinstance(ltype, ResolvedConcreteType) TODO?

        if not isinstance(ltype, ResolvedConcreteType):
            return TypeVariable()

        # if mdecl := ltype.members.get(name):
        #     attr = mdecl.type
        #     if getattr(attr, "is_python_func", False):
        #         attr.python_func_used = True
        #     return attr
        # if meth := ltype.methods.get(name):
        #     meth = meth.gen_sub(ltype, {})
        #     if bound:
        #         return meth.remove_self()
        #     else:
        #         return meth
        if field := ltype.fields.get(name):
            ty = field.type.resolve()
            # if getattr(ty, "is_python_func", False):
            #     ty.python_func_used = True
            if isinstance(ty, MethodType):
                if bound and field.in_class_def and type(field.val) != RuntimeValue:
                    return ty.remove_self(ltype)
            return ty


        from transpiler.phases.typing.exceptions import MissingAttributeError
        parents = iter(ltype.get_mro())
        next(parents)
        for p in parents:
            try:
                return self.visit_getattr(p, name)
            except MissingAttributeError as e:
                pass
        # class MemberProtocol(TypeOperator):
        #     pass
        raise MissingAttributeError(ltype, name)

    def visit_List(self, node: ast.List) -> BaseType:
        if not node.elts:
            return TY_LIST.instantiate_default()
        elems = [self.visit(e) for e in node.elts]
        first, *rest = elems
        for e in rest:
            try:
                first.unify(e)
            except:
                raise NotImplementedError(f"List with different types not handled yet: {', '.join(map(str, elems))}")
        return TY_LIST.instantiate([elems[0]])

    def visit_Set(self, node: ast.Set) -> BaseType:
        if not node.elts:
            return TY_SET.instantiate_default()
        elems = [self.visit(e) for e in node.elts]
        if len(set(elems)) != 1:
            raise NotImplementedError("Set with different types not handled yet")
        return TY_SET.instantiate([elems[0]])

    def visit_Dict(self, node: ast.Dict) -> BaseType:
        if not node.keys:
            return TY_DICT.instantiate_default()
        key_type = TypeVariable()
        value_type = TypeVariable()
        for k, v in zip(node.keys, node.values):
            if not key_type.try_assign(self.visit(k)):
                raise NotImplementedError(f"Dict with different key types not handled yet in `{ast.unparse(node)}`")
            if not value_type.try_assign(self.visit(v)):
                raise NotImplementedError(f"Dict with different value types not handled yet in `{ast.unparse(node)}`")
        return TY_DICT.instantiate([key_type, value_type])

    def visit_Subscript(self, node: ast.Subscript) -> BaseType:
        left = self.visit(node.value)
        if isinstance(left, ClassTypeType):
            return self.anno().visit(node).type_type()
        raise NotImplementedError("Should not happen")
        # desugared
        # args = node.slice if type(node.slice) == tuple else [node.slice]
        # args = [self.visit(e) for e in args]
        # return self.make_dunder([left, *args], "getitem")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> BaseType:
        val = self.visit(node.operand)
        if isinstance(node.op, ast.Not):
            return TY_BOOL
        return self.make_dunder([val], DUNDER[type(node.op)])

    def visit_IfExp(self, node: ast.IfExp) -> BaseType:
        self.visit(node.test)
        then = self.visit(node.body)
        else_ = self.visit(node.orelse)
        if then != else_:
            raise NotImplementedError("IfExp with different types not handled yet")
        return then

    def make_dunder(self, args: List[BaseType], name: str) -> BaseType:
        return self.visit_function_call(
            self.visit_getattr(args[0], f"__{name}__"),
            args[1:]
        )

    def visit_ListComp(self, node: ast.ListComp) -> BaseType:
        if len(node.generators) != 1:
            raise NotImplementedError("Multiple generators not handled yet")
        gen: ast.comprehension = node.generators[0]
        iter_type = self.get_iter(self.visit(gen.iter))
        node.input_item_type = self.get_next(iter_type)
        virt_scope = self.scope.child(ScopeKind.FUNCTION)
        from transpiler.phases.typing.block import ScoperBlockVisitor
        visitor = ScoperBlockVisitor(virt_scope)
        visitor.visit_assign_target(gen.target, node.input_item_type)
        node.item_type = visitor.expr().visit(node.elt)
        # for if_ in gen.ifs:
        #     visitor.expr().visit(if_)
        gen.ifs_node = ast.BoolOp(ast.And(), gen.ifs, **linenodata(node))
        visitor.expr().visit(gen.ifs_node)
        return TY_LIST.instantiate([node.item_type])