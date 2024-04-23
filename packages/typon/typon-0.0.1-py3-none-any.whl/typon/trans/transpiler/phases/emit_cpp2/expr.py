# coding: utf-8
import ast
from dataclasses import dataclass, field
from typing import List, Iterable

from transpiler.phases.typing.types import UserType, FunctionType, Promise, TypeType, GenericUserType, \
    MonomorphizedUserType
from transpiler.phases.utils import make_lnd
from transpiler.utils import compare_ast, linenodata
from transpiler.phases.emit_cpp.consts import SYMBOLS, PRECEDENCE_LEVELS, DUNDER_SYMBOLS
from transpiler.phases.emit_cpp import CoroutineMode, join, NodeVisitor
from transpiler.phases.typing.scope import Scope, VarKind


class PrecedenceContext:
    def __init__(self, visitor: "ExpressionVisitor", op: str):
        self.visitor = visitor
        self.op = op

    def __enter__(self):
        self.visitor.precedence.append(self.op)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.visitor.precedence.pop()


# noinspection PyPep8Naming
@dataclass
class ExpressionVisitor(NodeVisitor):
    scope: Scope
    generator: CoroutineMode
    precedence: List = field(default_factory=list)

    def visit(self, node):
        if type(node) in SYMBOLS:
            yield SYMBOLS[type(node)]
        else:
            yield from NodeVisitor.visit(self, node)

    def prec_ctx(self, op: str) -> PrecedenceContext:
        """
        Creates a context manager that sets the precedence of the next expression.
        """
        return PrecedenceContext(self, op)

    def prec(self, op: str) -> "ExpressionVisitor":
        """
        Sets the precedence of the next expression.
        """
        return ExpressionVisitor(self.scope, self.generator, [op])

    def reset(self) -> "ExpressionVisitor":
        """
        Resets the precedence stack.
        """
        return ExpressionVisitor(self.scope, self.generator)

    def visit_Tuple(self, node: ast.Tuple) -> Iterable[str]:
        yield "std::make_tuple("
        yield from join(", ", map(self.visit, node.elts))
        yield ")"

    def visit_Constant(self, node: ast.Constant) -> Iterable[str]:
        if isinstance(node.value, str):
            # TODO: escape sequences
            yield f"\"{repr(node.value)[1:-1]}\"_ps"
        elif isinstance(node.value, bool):
            yield str(node.value).lower()
        elif isinstance(node.value, int):
            # TODO: bigints
            yield str(node.value)
        elif isinstance(node.value, float):
            yield repr(node.value)
        elif isinstance(node.value, complex):
            yield f"TyComplex({node.value.real}, {node.value.imag})"
        elif node.value is None:
            yield "PyNone"
        else:
            raise NotImplementedError(node, type(node))

    def visit_Slice(self, node: ast.Slice) -> Iterable[str]:
        yield "TySlice("
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
        with self.prec_ctx(cpp_op):
            yield from self.visit_binary_operation(cpp_op, node.values[0], node.values[1], make_lnd(node.values[0], node.values[1]))
            for left, right in zip(node.values[1:], node.values[2:]):
                yield f" {cpp_op} "
                yield from self.visit_binary_operation(cpp_op, left, right, make_lnd(left, right))

    def visit_Call(self, node: ast.Call) -> Iterable[str]:
        # TODO
        # if getattr(node, "keywords", None):
        #     raise NotImplementedError(node, "keywords")
        if getattr(node, "starargs", None):
            raise NotImplementedError(node, "varargs")
        if getattr(node, "kwargs", None):
            raise NotImplementedError(node, "kwargs")
        func = node.func
        if isinstance(func, ast.Attribute):
            if sym := DUNDER_SYMBOLS.get(func.attr, None):
                if len(node.args) == 1:
                    yield from self.visit_binary_operation(sym, func.value, node.args[0], linenodata(node))
                else:
                    yield from self.visit_unary_operation(sym, func.value)
                return
        for name in ("fork", "future"):
            if compare_ast(func, ast.parse(name, mode="eval").body):
                assert len(node.args) == 1
                arg = node.args[0]
                assert isinstance(arg, ast.Lambda)
                node.is_future = name
                vis = self.reset()
                vis.generator = CoroutineMode.SYNC
                # todo: bad code
                if CoroutineMode.ASYNC in self.generator:
                    yield f"co_await typon::{name}("
                    yield from vis.visit(arg.body)
                    yield ")"
                    return
                elif CoroutineMode.FAKE in self.generator:
                    yield from self.visit(arg.body)
                return
        if compare_ast(func, ast.parse('sync', mode="eval").body):
            if CoroutineMode.ASYNC in self.generator:
                yield "co_await typon::Sync()"
            elif CoroutineMode.FAKE in self.generator:
                yield from ()
            return
        # TODO: precedence needed?
        if CoroutineMode.ASYNC in self.generator and node.is_await:
            yield "("  # TODO: temporary
            yield "co_await "
            node.in_await = True
        elif CoroutineMode.FAKE in self.generator:
            func = ast.Attribute(value=func, attr="sync", ctx=ast.Load())
        yield from self.prec("()").visit(func)
        yield "("
        yield from join(", ", map(self.reset().visit, node.args))
        yield ")"
        if CoroutineMode.ASYNC in self.generator and node.is_await:
            yield ")"

    def visit_Lambda(self, node: ast.Lambda) -> Iterable[str]:
        yield "[]"
        templ, args, _ = self.process_args(node.args)
        yield templ
        yield args
        yield "{"
        yield "return"
        yield from self.reset().visit(node.body)
        yield ";"
        yield "}"

    def visit_BinOp(self, node: ast.BinOp) -> Iterable[str]:
        yield from self.visit_binary_operation(node.op, node.left, node.right, linenodata(node))

    def visit_Compare(self, node: ast.Compare) -> Iterable[str]:
        yield from self.visit_binary_operation(node.ops[0], node.left, node.comparators[0], linenodata(node))

    def visit_binary_operation(self, op, left: ast.AST, right: ast.AST, lnd: dict) -> Iterable[str]:
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
            yield "typon::TyList{"
            yield from join(", ", map(self.reset().visit, node.elts))
            yield "}"
        else:
            yield from self.visit(node.type)
            yield "{}"

    def visit_Set(self, node: ast.Set) -> Iterable[str]:
        if node.elts:
            yield "typon::TySet{"
            yield from join(", ", map(self.reset().visit, node.elts))
            yield "}"
        else:
            yield from self.visit(node.type)
            yield "{}"

    def visit_Dict(self, node: ast.Dict) -> Iterable[str]:
        def visit_item(key, value):
            yield "std::pair {"
            yield from self.reset().visit(key)
            yield ", "
            yield from self.reset().visit(value)
            yield "}"

        if node.keys:
            yield from self.visit(node.type)
            yield "{"
            yield from join(", ", map(visit_item, node.keys, node.values))
            yield "}"
        else:
            yield from self.visit(node.type)
            yield "{}"

    def visit_Subscript(self, node: ast.Subscript) -> Iterable[str]:
        if isinstance(node.type, TypeType) and isinstance(node.type.type_object, MonomorphizedUserType):
            yield node.type.type_object.name
            return
        yield from self.prec("[]").visit(node.value)
        yield "["
        yield from self.reset().visit(node.slice)
        yield "]"

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Iterable[str]:
        yield from self.visit_unary_operation(node.op, node.operand)

    def visit_unary_operation(self, op, operand) -> Iterable[str]:
        if type(op) != str:
            op = SYMBOLS[type(op)]
        yield op
        yield from self.prec("unary").visit(operand)

    def visit_IfExp(self, node: ast.IfExp) -> Iterable[str]:
        with self.prec_ctx("?:"):
            yield from self.visit(node.test)
            yield " ? "
            yield from self.visit(node.body)
            yield " : "
            yield from self.visit(node.orelse)

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
        yield "mapFilter([]("
        yield from self.visit(node.input_item_type)
        yield from self.visit(gen.target)
        yield ") { return "
        yield from self.visit(node.elt)
        yield "; }, "
        yield from self.visit(gen.iter)
        if gen.ifs:
            yield ", "
            yield "[]("
            yield from self.visit(node.input_item_type)
            yield from self.visit(gen.target)
            yield ") { return "
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