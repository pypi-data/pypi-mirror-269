# coding: utf-8
import ast
from dataclasses import dataclass, field
from typing import Iterable

from transpiler.phases.emit_cpp.visitors import NodeVisitor, CoroutineMode, join
from transpiler.phases.typing.scope import Scope
from transpiler.phases.typing.types import ClassTypeType, TupleInstanceType, TY_FUTURE, ResolvedConcreteType, TY_FORKED, \
    GenericInstanceType
from transpiler.phases.utils import make_lnd
from transpiler.utils import linenodata

SYMBOLS = {
    ast.Eq: "==",
    ast.NotEq: '!=',
    ast.Pass: '/* pass */',
    ast.Mult: '*',
    ast.Add: '+',
    ast.Sub: '-',
    ast.Div: '/',
    ast.FloorDiv: '/',  # TODO
    ast.Mod: '%',
    ast.Lt: '<',
    ast.Gt: '>',
    ast.GtE: '>=',
    ast.LtE: '<=',
    ast.LShift: '<<',
    ast.RShift: '>>',
    ast.BitXor: '^',
    ast.BitOr: '|',
    ast.BitAnd: '&',
    ast.Not: '!',
    ast.IsNot: '!=',
    ast.USub: '-',
    ast.And: '&&',
    ast.Or: '||'
}
"""Mapping of Python AST nodes to C++ symbols."""

# noinspection PyPep8Naming
@dataclass
class ExpressionVisitor(NodeVisitor):
    scope: Scope
    generator: CoroutineMode

    def visit(self, node):
        if False and type(node) in SYMBOLS:
            yield SYMBOLS[type(node)]
        else:
            yield from NodeVisitor.visit(self, node)

    def visit_Tuple(self, node: ast.Tuple) -> Iterable[str]:
        yield "std::make_tuple("
        yield from join(", ", map(self.visit, node.elts))
        yield ")"

    def visit_Constant(self, node: ast.Constant) -> Iterable[str]:
        if isinstance(node.value, str):
            # TODO: escape sequences
            yield f"\"{repr(node.value)[1:-1]}\"_ps"
        elif isinstance(node.value, bool):
            yield f"typon::TyBool({str(node.value).lower()})"
        elif isinstance(node.value, int):
            # TODO: bigints
            yield str(node.value) + "_pi"
        elif isinstance(node.value, float):
            yield repr(node.value)
        elif isinstance(node.value, complex):
            yield f"TyComplex({node.value.real}, {node.value.imag})"
        elif node.value is None:
            yield "None"
        else:
            raise NotImplementedError(node, type(node))

    def visit_Slice(self, node: ast.Slice) -> Iterable[str]:
        yield "typon::TySlice("
        yield from join(", ", (self.visit(x or ast.Constant(value=None)) for x in (node.lower, node.upper, node.step)))
        yield ")"

    def visit_Name(self, node: ast.Name) -> Iterable[str]:
        res = self.fix_name(node.id)
        if self.scope.function and (decl := self.scope.get(res)) and decl.type is self.scope.function.obj_type:
            if not self.scope.function.parent.function:
                res = "(*this)"
            #if decl.kind == VarKind.SELF:
            #    res = "(*this)"
            #elif decl.future and CoroutineMode.ASYNC in self.generator:
            #    res = f"{res}.get()"
            #    if decl.future == "future":
            #        res = "co_await " + res
        yield res

    # def visit_Compare(self, node: ast.Compare) -> Iterable[str]:
    #     def make_lnd(op1, op2):
    #         return {
    #             "lineno": op1.lineno,
    #             "col_offset": op1.col_offset,
    #             "end_lineno": op2.end_lineno,
    #             "end_col_offset": op2.end_col_offset
    #         }
    #
    #     operands = [node.left, *node.comparators]
    #     with self.prec_ctx("&&"):
    #         yield from self.visit_binary_operation(node.ops[0], operands[0], operands[1], make_lnd(operands[0], operands[1]))
    #         for (left, right), op in zip(zip(operands[1:], operands[2:]), node.ops[1:]):
    #             # TODO: cleaner code
    #             yield " && "
    #             yield from self.visit_binary_operation(op, left, right, make_lnd(left, right))

    def visit_BoolOp(self, node: ast.BoolOp) -> Iterable[str]:
        if len(node.values) == 1:
            yield from self.visit(node.values[0])
            return
        cpp_op = {
            ast.And: "&&",
            ast.Or: "||"
        }[type(node.op)]
        yield "("
        yield from self.visit_binary_operation(cpp_op, node.values[0], node.values[1], make_lnd(node.values[0], node.values[1]))
        for left, right in zip(node.values[1:], node.values[2:]):
            yield f" {cpp_op} "
            yield from self.visit_binary_operation(cpp_op, left, right, make_lnd(left, right))
        yield ")"

    def visit_Call(self, node: ast.Call) -> Iterable[str]:
        if isinstance(node.func, ast.Name) and node.func.id in ("fork", "future"):
            assert len(node.args) == 1
            arg = node.args[0]
            assert isinstance(arg, ast.Lambda)
            fixed = node.func.id
            if fixed == "future": # Temporary until we separate the namespaces
                fixed = "future_stdlib"
            if self.generator != CoroutineMode.SYNC:
                yield f"co_await typon::{fixed}("
                assert isinstance(arg.body, ast.Call)
                yield from self.visit(arg.body.func)
                yield "("
                yield from join(", ", map(self.visit, arg.body.args))
                yield ")"
                yield ")"
            else:
                match node.func.id:
                    case "fork":
                        yield from self.visit(arg.body) # fork is transparent
                    case "future":
                        yield "typon::future_stdlib.typon$$sync("
                        yield from self.visit(arg.body)
                        yield ")"

            return

        if isinstance(node.func, ast.Name) and node.func.id == "sync":
            if self.generator != CoroutineMode.SYNC:
                yield "co_await typon::Sync()"
            else:
                yield "(void)0"
            return


        is_get = isinstance(node.func, ast.Attribute) and node.func.attr == "get"

        # async : co_await f(args)
        # sync : call_sync(f, args)
        if self.generator != CoroutineMode.SYNC:
            nty = node.type.resolve()
            if isinstance(nty, ResolvedConcreteType) and (
                #nty.inherits(TY_FUTURE) or
                (
                    is_get and nty.inherits(TY_FORKED)
                )
            ):
                pass
            else:
                yield "co_await"
        else:
            if is_get and node.func.value.type.inherits(TY_FORKED):
                yield from self.visit(node.func.value)
                return
            elif is_get and node.func.value.type.inherits(TY_FUTURE):
                yield "(typename std::remove_cvref_t<decltype(*"
                yield from self.visit(node.func.value)
                yield ".operator->())>::promise_type::value_type{})"
                return
            else:
                yield "call_sync"




        yield "("

        if is_get and node.func.value.type.inherits(TY_FUTURE, TY_FORKED):
            yield "("
            yield from self.visit(node.func.value)
            yield ")->get"
        else:
            yield from self.visit(node.func)

        yield ")"

        add_call = False

        if isinstance(node.func.type, ClassTypeType):
            inner = node.func.type.inner_type
            if isinstance(node.type, GenericInstanceType):
                assert inner is node.type.generic_parent
                yield ".template operator()"
                yield "<"
                yield from join(", ", (self.visit(arg) for arg in node.type.generic_args))
                yield ">"
                add_call = True


        yield "("
        yield from join(", ", map(self.visit, node.args))
        yield ")"

        if add_call and self.generator == CoroutineMode.SYNC:
            yield ".call()"
        #raise NotImplementedError()
        # TODO
        # if getattr(node, "keywords", None):
        #     raise NotImplementedError(node, "keywords")
        # if getattr(node, "starargs", None):
        #     raise NotImplementedError(node, "varargs")
        # if getattr(node, "kwargs", None):
        #     raise NotImplementedError(node, "kwargs")
        # func = node.func
        # if isinstance(func, ast.Attribute):
        #     if sym := DUNDER_SYMBOLS.get(func.attr, None):
        #         if len(node.args) == 1:
        #             yield from self.visit_binary_operation(sym, func.value, node.args[0], linenodata(node))
        #         else:
        #             yield from self.visit_unary_operation(sym, func.value)
        #         return
        # for name in ("fork", "future"):
        #     if compare_ast(func, ast.parse(name, mode="eval").body):
        #         assert len(node.args) == 1
        #         arg = node.args[0]
        #         assert isinstance(arg, ast.Lambda)
        #         node.is_future = name
        #         vis = self.reset()
        #         vis.generator = CoroutineMode.SYNC
        #         # todo: bad code
        #         if CoroutineMode.ASYNC in self.generator:
        #             yield f"co_await typon::{name}("
        #             yield from vis.visit(arg.body)
        #             yield ")"
        #             return
        #         elif CoroutineMode.FAKE in self.generator:
        #             yield from self.visit(arg.body)
        #         return
        # if compare_ast(func, ast.parse('sync', mode="eval").body):
        #     if CoroutineMode.ASYNC in self.generator:
        #         yield "co_await typon::Sync()"
        #     elif CoroutineMode.FAKE in self.generator:
        #         yield from ()
        #     return
        # # TODO: precedence needed?
        # if CoroutineMode.ASYNC in self.generator and node.is_await:
        #     yield "("  # TODO: temporary
        #     yield "co_await "
        #     node.in_await = True
        # elif CoroutineMode.FAKE in self.generator:
        #     func = ast.Attribute(value=func, attr="sync", ctx=ast.Load())
        # yield from self.prec("()").visit(func)
        # yield "("
        # yield from join(", ", map(self.reset().visit, node.args))
        # yield ")"
        # if CoroutineMode.ASYNC in self.generator and node.is_await:
        #     yield ")"

    def visit_Lambda(self, node: ast.Lambda) -> Iterable[str]:
        yield "[]"
        templ, args, _ = self.process_args(node.args)
        yield templ
        yield args
        yield "-> typon::Task<"
        yield from self.visit(node.type.deref().return_type)
        yield "> {"
        yield "co_return"
        yield from self.visit(node.body)
        yield ";"
        yield "}"

    def visit_BinOp(self, node: ast.BinOp) -> Iterable[str]:

        yield from self.visit_binary_operation(node.op, node.left, node.right, linenodata(node))

    def visit_Compare(self, node: ast.Compare) -> Iterable[str]:
        yield from self.visit_binary_operation(node.ops[0], node.left, node.comparators[0], linenodata(node))

    def visit_binary_operation(self, op, left: ast.AST, right: ast.AST, lnd: dict) -> Iterable[str]:
        if self.generator != CoroutineMode.SYNC:
            yield "(co_await"
        yield "("
        yield from self.visit(left)
        yield " "
        yield SYMBOLS[type(op)]
        yield " "
        yield from self.visit(right)
        yield ")"
        if self.generator != CoroutineMode.SYNC:
            yield ")"
        return
        raise NotImplementedError()
        # if type(op) == ast.In:
        #     call = ast.Call(ast.Attribute(right, "__contains__", **lnd), [left], [], **lnd)
        #     call.is_await = False
        #     yield from self.visit_Call(call)
        #     print(call.func.type)
        #     return
        if type(op) != str:
            op = SYMBOLS[type(op)]
        # TODO: handle precedence locally since only binops really need it
        # we could just store the history of traversed nodes and check if the last one was a binop
        prio = self.precedence and PRECEDENCE_LEVELS[self.precedence[-1]] < PRECEDENCE_LEVELS[op]
        if prio:
            yield "("
        with self.prec_ctx(op):
            yield from self.visit(left)
            yield op
            yield from self.visit(right)
        if prio:
            yield ")"

    def visit_Attribute(self, node: ast.Attribute) -> Iterable[str]:
        yield "dot"
        yield "(("
        yield from self.visit(node.value)
        yield "), "
        yield self.fix_name(node.attr)
        yield ")"

    def visit_List(self, node: ast.List) -> Iterable[str]:
        if node.elts:
            yield "typon::TyList({"
            yield from join(", ", map(self.visit, node.elts))
            yield "})"
        else:
            yield from self.visit(node.type)
            yield "{}"

    def visit_Set(self, node: ast.Set) -> Iterable[str]:
        if node.elts:
            yield "typon::TySet{"
            yield from join(", ", map(self.visit, node.elts))
            yield "}"
        else:
            yield from self.visit(node.type)
            yield "{}"

    def visit_Dict(self, node: ast.Dict) -> Iterable[str]:
        def visit_item(key, value):
            yield "{"
            yield from self.visit(key)
            yield ", "
            yield from self.visit(value)
            yield "}"

        if node.keys:
            yield from self.visit(node.type)
            #yield "typon::TyDict("
            yield "({"
            yield from join(", ", map(visit_item, node.keys, node.values))
            yield "})"
        else:
            yield from self.visit(node.type)
            yield "{}"

    def visit_Subscript(self, node: ast.Subscript) -> Iterable[str]:
        if isinstance(node.type, ClassTypeType):
            yield from self.visit_BaseType(node.type.inner_type)
            return

        if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, int):
            # when the index is a constant, we special case the emitted code so we can use std::get
            # if the subscripted object is a tuple because tuples are not subscriptable in C++ because
            # the language is statically typed
            yield "(co_await typon::constant_get<"
            yield str(node.slice.value)
            yield ">("
            yield from self.visit(node.value)
            yield "))"
            return
        # yield "("
        # yield from self.visit(node.value)
        # yield ")["
        # yield from self.visit(node.slice)
        # yield "]"
        yield "(co_await dot("
        yield from self.visit(node.value)
        yield ", oo__getitem__oo)("
        yield from self.visit(node.slice)
        yield "))"

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Iterable[str]:
        yield from self.visit_unary_operation(node.op, node.operand)

    def visit_unary_operation(self, op, operand) -> Iterable[str]:
        if type(op) != str:
            op = SYMBOLS[type(op)]
        yield "("
        yield op
        yield from self.visit(operand)
        yield ")"

    def visit_IfExp(self, node: ast.IfExp) -> Iterable[str]:
        yield "("
        yield from self.visit(node.test)
        yield " ? "
        yield from self.visit(node.body)
        yield " : "
        yield from self.visit(node.orelse)
        yield ")"

    def visit_Yield(self, node: ast.Yield) -> Iterable[str]:
        #if CoroutineMode.GENERATOR in self.generator:
        #    yield "co_yield"
        #    yield from self.prec("co_yield").visit(node.value)
        #elif CoroutineMode.FAKE in self.generator:
        #    yield "return"
        #    yield from self.visit(node.value)
        #else:
        #    raise NotImplementedError(node)
        yield "co_yield"
        yield from self.prec("co_yield").visit(node.value)

    def visit_ListComp(self, node: ast.ListComp) -> Iterable[str]:
        if len(node.generators) != 1:
            raise NotImplementedError("Multiple generators not handled yet")
        gen: ast.comprehension = node.generators[0]
        yield "MAP_FILTER("
        yield from self.visit(gen.target)
        yield ","
        yield from self.visit(gen.iter)
        yield ", "
        yield from self.visit(node.elt)
        yield ", "
        if gen.ifs:
            yield from self.visit(gen.ifs_node)
        else:
            yield "true"
        yield ")"

        return
        yield "mapFilter([]("
        #yield from self.visit(node.input_item_type)
        yield "auto"
        yield from self.visit(gen.target)
        yield ") { return "
        yield from self.visit(node.elt)
        yield "; }, "
        yield from self.visit(gen.iter)
        if gen.ifs:
            yield ", "
            yield "[]("
            #yield from self.visit(node.input_item_type)
            yield "auto"
            yield from self.visit(gen.target)
            yield ") -> typon::Task<"
            yield from self.visit(gen.ifs_node.type)
            yield "> { return "
            yield from self.visit(gen.ifs_node)
            yield "; }"
        yield ")"
        # iter_type = get_iter(self.visit(gen.iter))
        # next_type = get_next(iter_type)
        # virt_scope = self.scope.child(ScopeKind.FUNCTION_INNER)
        # from transpiler import ScoperBlockVisitor
        # visitor = ScoperBlockVisitor(virt_scope)
        # visitor.visit_assign_target(gen.target, next_type)
        # res_item_type = visitor.expr().visit(node.elt)
        # for if_ in gen.ifs:
        #     visitor.expr().visit(if_)
        # return TyList(res_item_type)