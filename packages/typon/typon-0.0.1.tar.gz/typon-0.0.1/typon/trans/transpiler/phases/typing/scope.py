import ast
from dataclasses import field, dataclass
from enum import Enum
from typing import Optional, Dict, List, Any, Self

from transpiler.phases.typing.types import BaseType, RuntimeValue


class VarKind(Enum):
    """Kind of variable."""
    LOCAL = 1
    """`xxx = ...`"""
    GLOBAL = 2
    """`global xxx"""
    NONLOCAL = 3
    """`nonlocal xxx`"""
    SELF = 4
    OUTER_DECL = 5
    MODULE = 6


class VarType:
    pass


@dataclass
class VarDecl:
    kind: VarKind
    type: BaseType
    val: Any = RuntimeValue()
    is_item_decl: bool = False
    from_node: ast.AST = None


class ScopeKind(Enum):
    GLOBAL = 1
    """Global (module) scope"""
    FUNCTION = 2
    """Function scope"""
    FUNCTION_INNER = 3
    """Block (if, for, ...) scope inside a function"""
    CLASS = 4
    """Class scope"""


@dataclass
class Scope:
    parent: Optional["Scope"] = None
    kind: ScopeKind = ScopeKind.GLOBAL
    function: Optional["Scope"] = None
    global_scope: Optional["Scope"] = None
    vars: Dict[str, VarDecl] = field(default_factory=dict)
    children: List["Scope"] = field(default_factory=list)
    obj_type: Optional[BaseType] = None
    diverges: bool = False
    class_: Optional["Scope"] = None
    is_loop: Optional[ast.For | ast.While] = None
    root_decls: Dict[str, ast.expr] = field(default_factory=dict)

    @staticmethod
    def make_global():
        res = Scope()
        res.global_scope = res
        return res

    def is_in_loop(self) -> Optional[ast.For | ast.While]:
        if self.is_loop:
            return self.is_loop
        if self.parent is not None and self.kind != ScopeKind.FUNCTION:
            return self.parent.is_in_loop()
        return None

    def child(self, kind: ScopeKind) -> Self:
        res = Scope(self, kind, self.function, self.global_scope)
        if kind == ScopeKind.GLOBAL:
            res.global_scope = res
        self.children.append(res)
        return res

    def declare_local(self, name: str, type: BaseType):
        """Declares a local variable"""
        self.vars[name] = VarDecl(VarKind.LOCAL, type)

    def get(self, name: str, kind: VarKind | set[VarKind] = VarKind.LOCAL, restrict_function: bool = False) -> Optional[VarDecl]:
        """
        Gets the variable declaration of a variable in the current scope or any parent scope.
        """
        if type(kind) is VarKind:
            kind = {kind}
        if (res := self.vars.get(name)) and res.kind in kind:
            if res.kind == VarKind.GLOBAL:
                return self.global_scope.get(name, kind)
            elif res.kind == VarKind.NONLOCAL:
                return self.function.parent.get(name, VarKind.LOCAL, True)
            return res
        if self.parent is not None and not (self.kind == ScopeKind.FUNCTION and restrict_function):
            return self.parent.get(name, kind, restrict_function)
        return None
