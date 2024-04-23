import ast
from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from transpiler.phases.typing.expr import ScoperExprVisitor
from transpiler.utils import highlight
from transpiler.phases.typing.annotations import TypeAnnotationVisitor
from transpiler.phases.typing.scope import Scope, ScopeKind, VarDecl, VarKind
from transpiler.phases.typing.types import BaseType, TypeVariable, TY_NONE, BuiltinFeatureType, ClassTypeType
from transpiler.phases.utils import NodeVisitorSeq, AnnotationName

PRELUDE = Scope.make_global()


@dataclass
class ScoperVisitor(NodeVisitorSeq):
    scope: Scope = field(default_factory=lambda: PRELUDE.child(ScopeKind.GLOBAL))
    root_decls: Dict[str, VarDecl] = field(default_factory=dict)

    def expr(self) -> "ScoperExprVisitor":
        from transpiler.phases.typing.expr import ScoperExprVisitor
        return ScoperExprVisitor(self.scope, self.root_decls)

    def anno(self) -> "TypeAnnotationVisitor":
        return TypeAnnotationVisitor(self.scope)

    def visit_annotation(self, expr: Optional[ast.expr]) -> BaseType:
        res = self.anno().visit(expr) if expr else TypeVariable()
        assert not isinstance(res, ClassTypeType)
        return res

    def annotate_arg(self, arg: ast.arg) -> BaseType:
        if arg.annotation is None or isinstance(arg.annotation, AnnotationName):
            res = TypeVariable()
            arg.annotation = AnnotationName(res)
            return res
        else:
            return self.visit_annotation(arg.annotation)

    def parse_function(self, node: ast.FunctionDef):
        argtypes = [self.annotate_arg(arg) for arg in node.args.args]
        rtype = self.visit_annotation(node.returns)
        ftype = FunctionType(argtypes, rtype)
        scope = self.scope.child(ScopeKind.FUNCTION)
        scope.obj_type = ftype
        scope.function = scope
        node.inner_scope = scope
        node.type = ftype
        ftype.optional_at = len(node.args.args) - len(node.args.defaults)
        for ty, default in zip(argtypes[ftype.optional_at:], node.args.defaults):
            self.expr().visit(default).unify(ty)
        for arg, ty in zip(node.args.args, argtypes):
            scope.vars[arg.arg] = VarDecl(VarKind.LOCAL, ty)
        self.fdecls.append((node, rtype))
        return ftype

    def visit_block(self, block: list[ast.AST]):
        if not block:
            return
        __TB__ = f"running type analysis on block starting with {highlight(block[0])}"
        self.fdecls = []
        for b in block:
            self.visit(b)
        if self.fdecls:
            old_list = self.fdecls
            exc = None
            while True:
                new_list = []
                for node, rtype in old_list:
                    from transpiler.exceptions import CompileError
                    try:
                        self.visit_function_definition(node, rtype)
                    except CompileError as e:
                        new_list.append((node, rtype))
                        if not exc or getattr(node, "is_main", False):
                            exc = e
                if len(new_list) == len(old_list):
                    raise exc
                if not new_list:
                    break
                old_list = new_list
                exc = None

    def visit_function_definition(self, node, rtype):
        __TB__ = f"running type analysis on the body of {highlight(node)}"
        __TB_NODE__ = node
        from transpiler.phases.typing.block import ScoperBlockVisitor
        for b in node.body:
            decls = {}
            visitor = ScoperBlockVisitor(node.inner_scope, decls)
            visitor.fdecls = []
            visitor.visit(b)
            if len(visitor.fdecls) > 1:
                raise NotImplementedError("?")
            elif len(visitor.fdecls) == 1:
                fnode, frtype = visitor.fdecls[0]
                self.visit_function_definition(fnode, frtype)
                # del node.inner_scope.vars[fnode.name]
                visitor.visit_assign_target(ast.Name(fnode.name), fnode.type)
            b.decls = decls
        if not node.inner_scope.diverges and not (
                isinstance(node.type.return_type, Promise) and node.type.return_type.kind == PromiseKind.GENERATOR):
            from transpiler.phases.typing.exceptions import TypeMismatchError
            try:
                rtype.unify(TY_NONE)
            except TypeMismatchError as e:
                from transpiler.phases.typing.exceptions import MissingReturnError
                raise MissingReturnError(node) from e

    def get_iter(self, seq_type):
        try:
            return self.expr().visit_function_call(self.expr().visit_getattr(seq_type, "__iter__"), [])
        except:
            from transpiler.phases.typing.exceptions import NotIterableError
            raise NotIterableError(seq_type)

    def get_next(self, iter_type):
        try:
            return self.expr().visit_function_call(self.expr().visit_getattr(iter_type, "__next__"), [])
        except:
            from transpiler.phases.typing.exceptions import NotIterableError
            raise NotIterableError(iter_type)


def is_builtin(x, feature):
    return isinstance(x, BuiltinFeatureType) and x.feature() == feature


@dataclass
class DeclareInfo:
    detail: bool | list[bool]
    initial_value: Optional[ast.expr] = None


IsDeclare = None | DeclareInfo
