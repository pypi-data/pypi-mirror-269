import ast
from dataclasses import dataclass, field
from typing import Iterable, Optional

from transpiler.phases.emit_cpp.expr import ExpressionVisitor
from transpiler.phases.typing.common import IsDeclare
from transpiler.phases.typing.scope import Scope
from transpiler.phases.emit_cpp.visitors import NodeVisitor, flatmap, CoroutineMode, join
from transpiler.phases.typing.types import CallableInstanceType, BaseType, TypeVariable
from transpiler.phases.utils import PlainBlock


def emit_function(name: str, func: CallableInstanceType, base="function", gen_p=None) -> Iterable[str]:
    __TB_NODE__ = func.block_data.node
    yield f"struct : referencemodel::{base} {{"
    def emit_body(name: str, mode: CoroutineMode, rty):
        #real_params = [p for p in func.generic_parent.parameters if not p.name.startswith("AutoVar$")]
        if func.generic_parent.parameters:
            yield "template<"
            yield from join(",", (f"typename {p.name} = void" for p in func.generic_parent.parameters))
            yield ">"
        yield "auto"
        yield name
        yield "("
        def emit_arg(arg, ty):
            __TB_NODE__ = arg
            if isinstance(ty, TypeVariable) and ty.emit_as_is:
                yield ty.var_name
            else:
                raise NotImplementedError("can this happen?")
                yield "auto"
            yield arg.arg

        yield from join(",", (emit_arg(arg, ty) for arg, ty in zip(func.block_data.node.args.args, func.parameters)))

        yield ") const"
        if rty is not None:
            yield "->"
            yield rty
        yield " {"
        for var, initval in func.block_data.scope.root_decls.items():
            __TB_NODE__ = initval
            if isinstance(initval, BaseType):
                yield from NodeVisitor().visit_BaseType(initval)
            else:
                yield "typename std::remove_reference<decltype(" # TODO: duplicate code in visit_lvalue
                yield from ExpressionVisitor(func.block_data.scope, mode).visit(initval)
                yield ")>::type"
            yield var
            yield ";"
        __TB_NODE__ = func.block_data.node
        vis = BlockVisitor(func.block_data.scope, generator=mode)
        for stmt in func.block_data.node.body:
            yield from vis.visit(stmt)
        if not getattr(func.block_data.scope, "has_return", False):
            if mode == CoroutineMode.SYNC:
                yield "return"
            else:
                yield "co_return"
            yield "{};"
        yield "}"

    rty = func.return_type.generic_args[0]
    has_sync = False
    try:
        rty_code = " ".join(NodeVisitor().visit_BaseType(func.return_type))
    except:
        yield from emit_body("typon$$sync", CoroutineMode.SYNC, None)
        has_sync = True
        yield "using has_sync = std::true_type;"
        def task_type():
            yield from NodeVisitor().visit_BaseType(func.return_type.generic_parent)
            yield "<"
            yield"decltype(typon$$sync<"
            yield from join(",", (p.name for p in func.generic_parent.parameters))
            yield ">("
            yield from join(",", (arg.arg for arg in func.block_data.node.args.args))
            yield "))"
            yield ">"
        rty_code = " ".join(task_type())
    else:
        pass

    yield from emit_body("operator()", CoroutineMode.TASK, rty_code)
    yield f"}} static constexpr {name} {{}};"
    if has_sync:
        yield f"static_assert(HasSync<decltype({name})>);"
    yield f"static_assert(sizeof {name} == 1);"



@dataclass
class BlockVisitor(NodeVisitor):
    scope: Scope
    generator: CoroutineMode = field(default=CoroutineMode.SYNC, kw_only=True)

    def expr(self) -> ExpressionVisitor:
        return ExpressionVisitor(self.scope, self.generator)

    def visit_PlainBlock(self, node: PlainBlock) -> Iterable[str]:
        yield from self.emit_block(node.inner_scope, node.body)

    def visit_Pass(self, node: ast.Pass) -> Iterable[str]:
        yield ";"

    def visit_Expr(self, node: ast.Expr) -> Iterable[str]:
        yield from self.expr().visit(node.value)
        yield ";"

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

    # def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[str]:
    #     yield from self.visit_free_func(node)

    # def visit_free_func(self, node: ast.FunctionDef, emission: FunctionEmissionKind) -> Iterable[str]:
    #     if getattr(node, "is_main", False):
    #         if emission == FunctionEmissionKind.DECLARATION:
    #             return
    #         # Special case handling for Python's interesting way of defining an entry point.
    #         # I mean, it's not *that* bad, it's just an attempt at retrofitting an "entry point" logic in a scripting
    #         # language that, by essence, uses "the start of the file" as the implicit entry point, since files are
    #         # read and executed line-by-line, contrary to usual structured languages that mark a distinction between
    #         # declarations (functions, classes, modules, ...) and code.
    #         # Also, for nitpickers, the C++ standard explicitly allows for omitting a `return` statement in the `main`.
    #         # 0 is returned by default.
    #         yield "typon::Root root() const"
    #
    #         def block():
    #             yield from node.body
    #             yield ast.Return()
    #
    #         from transpiler.phases.emit_cpp.function import FunctionVisitor
    #         yield "{"
    #         yield from self.visit_func_decls(block(), node.scope, CoroutineMode.TASK)
    #         yield "}"
    #         return
    #
    #     if emission == FunctionEmissionKind.DECLARATION:
    #         yield f"struct {node.name}_inner {{"
    #     yield from self.visit_func_new(node, emission)
    #     if emission == FunctionEmissionKind.DECLARATION:
    #         yield f"}} {node.name};"

    # def visit_func_decls(self, body: list[ast.stmt], inner_scope: Scope, mode = CoroutineMode.ASYNC) -> Iterable[str]:
    #     for child in body:
    #         from transpiler.phases.emit_cpp.function import FunctionVisitor
    #         child_visitor = FunctionVisitor(inner_scope, generator=mode)
    #
    #         for name, decl in getattr(child, "decls", {}).items():
    #             #yield f"decltype({' '.join(self.expr().visit(decl.type))}) {name};"
    #             yield from self.visit(decl.type)
    #             yield f" {name};"
    #         yield from child_visitor.visit(child)
    #
    # def visit_func_params(self, args: Iterable[tuple[str, BaseType, Optional[ast.expr]]], emission: FunctionEmissionKind) -> Iterable[str]:
    #     for i, (arg, argty, default) in enumerate(args):
    #         if i != 0:
    #             yield ", "
    #         if emission == FunctionEmissionKind.METHOD and i == 0:
    #             yield "Self"
    #         else:
    #             yield from self.visit(argty)
    #         yield arg
    #         if emission in {FunctionEmissionKind.DECLARATION, FunctionEmissionKind.LAMBDA, FunctionEmissionKind.METHOD} and default:
    #             yield " = "
    #             yield from self.expr().visit(default)
    #
    # def visit_func_new(self, node: ast.FunctionDef, emission: FunctionEmissionKind, skip_first_arg: bool = False) -> Iterable[str]:
    #     if emission == FunctionEmissionKind.LAMBDA:
    #         yield "[&]"
    #     else:
    #         if emission == FunctionEmissionKind.METHOD:
    #             yield "template <typename Self>"
    #         yield from self.visit(node.type.return_type)
    #         if emission == FunctionEmissionKind.DEFINITION:
    #             yield f"{node.name}_inner::"
    #         yield "operator()"
    #     yield "("
    #     padded_defaults = [None] * (len(node.args.args) if node.type.optional_at is None else node.type.optional_at) + node.args.defaults
    #     args_iter = zip(node.args.args, node.type.parameters, padded_defaults)
    #     if skip_first_arg:
    #         next(args_iter)
    #     yield from self.visit_func_params(((arg.arg, argty, default) for arg, argty, default in args_iter), emission)
    #     yield ")"
    #
    #     if emission == FunctionEmissionKind.METHOD:
    #         yield "const"
    #
    #     inner_scope = node.inner_scope
    #
    #     if emission == FunctionEmissionKind.DECLARATION:
    #         yield ";"
    #         return
    #
    #     if emission == FunctionEmissionKind.LAMBDA:
    #         yield "->"
    #         yield from self.visit(node.type.return_type)
    #
    #     yield "{"
    #
    #     class ReturnVisitor(SearchVisitor):
    #         def visit_Return(self, node: ast.Return) -> bool:
    #             yield True
    #
    #         def visit_Yield(self, node: ast.Yield) -> bool:
    #             yield True
    #
    #         def visit_FunctionDef(self, node: ast.FunctionDef):
    #             yield from ()
    #
    #         def visit_ClassDef(self, node: ast.ClassDef):
    #             yield from ()
    #
    #     has_return = ReturnVisitor().match(node.body)
    #
    #     yield from self.visit_func_decls(node.body, inner_scope)
    #
    #     # if not has_return and isinstance(node.type.return_type, Promise):
    #     #     yield "co_return;"
    #
    #     yield "}"
    #
    def visit_lvalue(self, lvalue: ast.expr, declare: IsDeclare, allow_auto: bool = False, annotation: ast.Expr = None) -> Iterable[str]:
        if isinstance(lvalue, ast.Tuple):
            # for name, decl, ty in zip(lvalue.elts, declare, lvalue.type.args):
            #     if decl:
            #         yield from self.visit_lvalue(name, True)
            #         yield ";"
            def helper(args):
                return self.visit_lvalue(*args)
            yield f"std::tie({', '.join(flatmap(helper, zip(lvalue.elts, declare.detail)))})"
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
                if allow_auto:
                    yield "auto"
                else:
                    if declare.initial_value:
                        yield "typename std::remove_reference<decltype("
                        yield from self.expr().visit(declare.initial_value)
                        yield ")>::type"
                    elif annotation is not None:
                        yield "typename std::remove_reference<decltype("
                        yield from self.expr().visit(annotation)
                        yield ")>::type::ObjType"
                    else:
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
        yield from self.visit_lvalue(node.targets[0], node.is_declare, True)
        yield " = "
        yield from self.expr().visit(node.value)
        yield ";"

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Iterable[str]:
        yield from self.visit_lvalue(node.target, node.is_declare, node.value is not None, node.annotation)
        if node.value:
            yield " = "
            yield from self.expr().visit(node.value)
        yield ";"

    def visit_Break(self, node: ast.Break) -> Iterable[str]:
        if (loop := self.scope.is_in_loop()).orelse:
            yield loop.orelse_variable
            yield " = false;"
        yield "break;"

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




    def emit_block(self, scope: Scope, items: Iterable[ast.stmt]) -> Iterable[str]:
        yield "{"
        for child in items:
            yield from BlockVisitor(scope, generator=self.generator).visit(child)
        yield "}"

    def visit_Return(self, node: ast.Return) -> Iterable[str]:
        if CoroutineMode.ASYNC in self.generator:
            yield "co_return "
        else:
            yield "return "
        if node.value:
            yield from self.expr().visit(node.value)
        else:
            yield "None"
        yield ";"


