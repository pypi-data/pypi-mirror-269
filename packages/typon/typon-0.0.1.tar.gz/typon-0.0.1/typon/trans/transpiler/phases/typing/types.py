import ast
import dataclasses
import enum
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Optional, Callable

from transpiler.utils import highlight


def get_default_parents():
    if obj := globals().get("TY_OBJECT"):
        return [obj]
    return []


class RuntimeValue:
    pass


@dataclass
class MemberDef:
    type: "BaseType"
    val: typing.Any = RuntimeValue()
    in_class_def: bool = True
    from_node: ast.AST = None

@dataclass
class UnifyMode:
    search_hierarchy: bool = True
    match_protocol: bool = True


UnifyMode.NORMAL = UnifyMode()
UnifyMode.EXACT = UnifyMode(False, False)

@dataclass
class BlockData[N]:
    node: N
    scope: "Scope"


@dataclass(eq=False)
class BaseType(ABC):
    block_data: Optional[BlockData] = field(default=None, init=False)

    def resolve(self) -> "BaseType":
        return self

    def type_type(self) -> "ClassTypeType":
        return TY_TYPE.instantiate([self.resolve()])

    @abstractmethod
    def name(self) -> str:
        ...

    def __str__(self):
        return self.name()

    @abstractmethod
    def unify_internal(self, other: "BaseType", mode: UnifyMode):
        pass

    def unify(self, other: "BaseType", mode = UnifyMode.NORMAL):
        a, b = self.resolve(), other.resolve()
        __TB__ = f"unifying {highlight(a)} and {highlight(b)}"
        if isinstance(b, TypeVariable):
            return b.unify_internal(a, mode)
            a, b = b, a
        a.unify_internal(b, mode)

    @abstractmethod
    def contains_internal(self, other: "BaseType") -> bool:
        pass

    def contains(self, other: "BaseType") -> bool:
        needle, haystack = other.resolve(), self.resolve()
        return (needle is haystack) or haystack.contains_internal(needle)

    def try_assign(self, other: "BaseType") -> bool:
        target, value = self.resolve(), other.resolve()
        if type(value) == TypeVariable:
            return BaseType.try_assign_internal(target, other)
        return target.try_assign_internal(other)


    def try_assign_internal(self, other: "BaseType") -> bool:
        try:
            self.unify(other)
            return True
        except:
            return False


    def deref(self):
        return self

cur_var = 0


def next_var_id():
    global cur_var
    cur_var += 1
    return cur_var

@dataclass(eq=False)
class ConcreteType(BaseType):
    """
    A concrete type is the type of a concrete value.

    It has fields and a list of parent concrete types.

    Examples: int, str, list[int]
    """


@dataclass(eq=False)
class TypeVariable(ConcreteType):
    var_name: str = field(default_factory=lambda: next_var_id())
    resolved: Optional[ConcreteType] = None
    emit_as_is: bool = False
    decltype_str: Optional[str] = None
    python_func_placeholder: bool = False

    def resolve(self) -> ConcreteType:
        if self.resolved is None:
            return self
        return self.resolved.resolve()

    def name(self):
        if self.resolved is None:
            # return f"TypeVar[\"{self.name}\"]"
            return f"_{self.var_name}"
        return str(self.resolved)

    def __eq__(self, other):
        if not isinstance(other, BaseType):
            return False
        if self.resolved is None:
            return self is other
        return self.resolved == other.resolve()

    def unify_internal(self, other: BaseType, mode: UnifyMode):
        if self is not other:
            if other.contains(self):
                from transpiler.phases.typing.exceptions import RecursiveTypeUnificationError
                raise RecursiveTypeUnificationError(self, other)

            self.resolved = other

            if isinstance(other, TypeVariable) and self.decltype_str != other.decltype_str:
                if (self.decltype_str and self.decltype_str.startswith("decltype")) and (other.decltype_str and other.decltype_str.startswith("decltype")):
                    pass
                elif (self.decltype_str and self.decltype_str.startswith("decltype")):
                    other.decltype_str = self.decltype_str

    def contains_internal(self, other: BaseType) -> bool:
        return self.resolve() is other.resolve()

    def deref(self):
        if self.resolved is None:
            return self
        return self.resolved.deref()



@dataclass(eq=False)
class ResolvedConcreteType(ConcreteType):
    """
    A concrete type is the type of a concrete value.

    It has fields and a list of parent concrete types.

    Examples: int, str, list[int]
    """

    fields: Dict[str, "MemberDef"] = field(default_factory=dict, init=False)
    parents: list["ResolvedConcreteType"] = field(default_factory=lambda: [TY_OBJECT], init=False)
    is_protocol: bool = field(default=False, init=False)

    def get_mro(self):
        """
        Performs linearization according to the MRO spec.

        https://www.python.org/download/releases/2.3/mro/
        """

        def remove_head_if(lst, head):
            if lst[0] == head:
                return lst[1:]
            return lst

        def merge(*lists):
            while True:
                lists = [l for l in lists if len(l) > 0]
                if len(lists) == 0:
                    return []
                for i, l in enumerate(lists):
                    head = l[0]
                    if not any(head in x[1:] for j, x in enumerate(lists) if i != j):
                        return [head] + merge(*[remove_head_if(x, head) for x in lists])
                else:
                    # couldn't find good head
                    from transpiler.phases.typing.exceptions import InconsistentMroError
                    raise InconsistentMroError(self.parents)

        return [self] + merge(*[p.get_mro() for p in self.parents], self.parents)

    def inherits(self, *parent: BaseType):
        return self in parent or any(p.inherits(*parent) for p in self.parents)

    def try_assign_internal(self, other: BaseType) -> bool:
        if self == other:
            return True

        if super().try_assign_internal(other):
            return True

        if self.is_protocol:
            if isinstance(other, TypeVariable):
                other.unify(self) # ? maybe, we'll see if it works
                return True
            assert isinstance(other, ResolvedConcreteType)
            for name, member in self.fields.items():
                corresponding = other.fields.get(name)
                if corresponding is None:
                    #raise ProtocolMismatchError(self, protocol, f"missing method {name}")
                    return False
                return member.type.deref().try_assign(corresponding.type.deref())

        return False

class UniqueTypeMixin:
    def unify_internal(self, other: "BaseType", mode: UnifyMode):
        from transpiler.phases.typing.exceptions import TypeMismatchError, TypeMismatchKind
        if other != self:
            raise TypeMismatchError(self, other, TypeMismatchKind.DIFFERENT_TYPE)

    def contains_internal(self, other: "BaseType") -> bool:
        return self == other

class BoundFuncTypeBase(UniqueTypeMixin):
    pass

@dataclass(eq=False)
class BuiltinType(UniqueTypeMixin, ResolvedConcreteType):
    pass

@dataclass(eq=False)
class UserType(BuiltinType):
    pass

@dataclass
class SpecialConstantType[T](ConcreteType):
    value: T

    def name(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, SpecialConstantType):
            return self.value == other.value
        return False


@dataclass(eq=False, init=False)
class GenericInstanceType(ResolvedConcreteType):
    """
    An instance of a generic type.

    Examples: list[int], dict[str, object], Callable[[int, int], int]
    """
    generic_parent: "GenericType" = field(init=False)
    generic_args: list[ConcreteType] = field(init=False)

    def __init__(self):
        super().__init__()

    def inherits(self, *parent: BaseType):
        return self.generic_parent in parent or super().inherits(*parent)

    def __eq__(self, other):
        if isinstance(other, GenericInstanceType):
            return self.generic_parent == other.generic_parent and self.generic_args == other.generic_args
        return False

    def name(self):
        return f"{self.generic_parent.name()}[{', '.join(map(str, self.generic_args))}]"

    def unify_internal(self, other: "BaseType", mode: UnifyMode):
        from transpiler.phases.typing.exceptions import TypeMismatchError, TypeMismatchKind
        if not isinstance(other, GenericInstanceType):
            raise TypeMismatchError(self, other, TypeMismatchKind.DIFFERENT_TYPE)
        if self.generic_parent != other.generic_parent:
            if not (isinstance(self, CallableInstanceType) and isinstance(other, CallableInstanceType)):
                # methods have different generic parent types but we don't really care
                raise TypeMismatchError(self, other, TypeMismatchKind.DIFFERENT_TYPE)
        if len(self.generic_args) != len(other.generic_args):
            raise TypeMismatchError(self, other, TypeMismatchKind.DIFFERENT_TYPE)
        for a, b in zip(self.generic_args, other.generic_args):
            a.unify(b, mode)

    def contains_internal(self, other: "BaseType") -> bool:
        # is this correct?
        return self == other or any(a.contains(other) for a in self.generic_args)

class PromiseKind(enum.Enum):
    TASK = 0
    JOIN = 1
    FUTURE = 2
    FORKED = 3
    GENERATOR = 4

class GenericParameterKind(enum.Enum):
    NORMAL = enum.auto()
    TUPLE = enum.auto()
    PARAMETERS = enum.auto()

@dataclass
class GenericParameter:
    name: str
    kind: GenericParameterKind = GenericParameterKind.NORMAL

gparam = GenericParameter

@dataclass
class GenericConstraint:
    left: ResolvedConcreteType
    right: ResolvedConcreteType


@dataclass(eq=False)
class GenericType(BaseType):
    parameters: list[GenericParameter] = field(default_factory=list, init=False)
    instance_cache: list[(object, GenericInstanceType)] = field(default_factory=list, init=False)

    def constraints(self, args: list[ConcreteType]) -> list[GenericConstraint]:
        return []

    @abstractmethod
    def _instantiate(self, args: list[ConcreteType]) -> GenericInstanceType:
        raise NotImplementedError()

    def instantiate(self, args: list[ConcreteType]) -> GenericInstanceType:
        __TB__ = f"instantiating {highlight(self.name())} with [{', '.join(map(highlight, map(str, args)))}]"
        res = self._instantiate(args)
        res.generic_args = args
        res.generic_parent = self
        return res

    def instantiate_default(self) -> GenericInstanceType:
        return self.instantiate([TypeVariable(decltype_str=p.name) for p in self.parameters])

    def __str__(self):
        try:
            default = self.instantiate_default()
            return "<" + ", ".join(str(arg.name()) for arg in default.generic_args) + "> " + str(default)
        except:
            return super().__str__()

    def deref(self):
        return self.instantiate_default().deref()

    def find_cached_instance(self, args):
        for inst_args, inst in self.instance_cache:
            if all(inst_arg.try_assign(arg) for inst_arg, arg in zip(inst_args, args)):
                return inst
        return None

    def cache_instance(self, args, instance):
        if not hasattr(self, "instance_cache"):
            self.instance_cache = []
        if not self.find_cached_instance(args):
            self.instance_cache.append((tuple(args), instance))

@dataclass(eq=False, init=False)
class BuiltinGenericType(UniqueTypeMixin, GenericType):
    constraints_: Callable[[list[ConcreteType]], list[GenericConstraint]]
    instantiate_: Callable[[list[ConcreteType]], GenericInstanceType]

    def constraints(self, args: list[ConcreteType]) -> list[GenericConstraint]:
        if not hasattr(self, "constraints_"):
            raise ValueError("missing constraints_")
        return self.constraints_(args)

    def _instantiate(self, args: list[ConcreteType]) -> GenericInstanceType:
        return self.instantiate_(args)


@dataclass(eq=False, init=False)
class UserGenericType(BuiltinGenericType):
    pass

def create_builtin_type(name: str, prefix="Builtin", base=BuiltinType):
    class CreatedType(base):
        def name(self):
            return name
    CreatedType.__name__ = f"{prefix}Type${name}"
    res = CreatedType()
    return res


TY_OBJECT = None
TY_OBJECT = create_builtin_type("object")
TY_OBJECT.parents = []
TY_BOOL = create_builtin_type("bool")
TY_INT = create_builtin_type("int")
TY_FLOAT = create_builtin_type("float")
TY_STR = create_builtin_type("str")
TY_BYTES = create_builtin_type("bytes")
TY_COMPLEX = create_builtin_type("complex")
TY_NONE = create_builtin_type("NoneType")


def unimpl(*args, **kwargs):
    raise NotImplementedError()


def create_builtin_generic_type(name: str, prefix="Builtin", base=BuiltinGenericType):
    class CreatedType(base):
        def name(self):
            return name
    CreatedType.__name__ = f"{prefix}GenericType${name}"
    res = CreatedType()
    return res

@dataclass(eq=False)
class TupleInstanceType(GenericInstanceType):
    fields: list[ConcreteType]


TY_LIST = create_builtin_generic_type("list")
TY_SET = create_builtin_generic_type("set")
TY_DICT = create_builtin_generic_type("dict")
TY_TUPLE = create_builtin_generic_type("tuple")
TY_SLICE = create_builtin_generic_type("slice")


TY_MUTEX = create_builtin_generic_type("Mutex")

# @dataclass(eq=False)
# class PromiseInstanceType(GenericInstanceType):
#     value: ConcreteType
#
#     def deref(self):
#         match self.generic_parent.kind:
#             case PromiseKind.TASK | PromiseKind.JOIN:
#                 return self.value.deref()
#             case _:
#                 return self
#
# @dataclass(eq=False)
# class PromiseType(UniqueTypeMixin, GenericType):
#     kind: PromiseKind
#
#     def name(self):
#         match self.kind:
#             case PromiseKind.TASK:
#                 return "Task"
#             case PromiseKind.JOIN:
#                 return "Join"
#             case PromiseKind.FUTURE:
#                 return "Future"
#             case PromiseKind.FORKED:
#                 return "Forked"
#             case PromiseKind.GENERATOR:
#                 return "Generator"
#
#     def _instantiate(self, args: list[ConcreteType]) -> GenericInstanceType:
#         assert len(args) == 1
#         return PromiseInstanceType(args[0])



# TY_TASK = PromiseType([GenericParameter("T")], PromiseKind.TASK)
# TY_JOIN = PromiseType([GenericParameter("T")], PromiseKind.JOIN)
# TY_FUTURE = PromiseType([GenericParameter("T")], PromiseKind.FUTURE)
# TY_FORKED = PromiseType([GenericParameter("T")], PromiseKind.FORKED)
# TY_GENERATOR = PromiseType([GenericParameter("T")], PromiseKind.GENERATOR)

TY_TASK = create_builtin_generic_type("Task")
TY_JOIN = create_builtin_generic_type("Join")
TY_FUTURE = create_builtin_generic_type("Future")
TY_FORKED = create_builtin_generic_type("Forked")
TY_GENERATOR = create_builtin_generic_type("Generator")

PROMISES = (TY_TASK, TY_JOIN, TY_FUTURE, TY_FORKED, TY_GENERATOR)
TRANSPARENT_PROMISES = (TY_TASK, TY_JOIN, TY_FUTURE)

TY_TUPLE.instantiate_ = lambda args: TupleInstanceType(args)

@dataclass(unsafe_hash=False)
class TypeTupleType(ConcreteType):
    """
    Special type used to represent a tuple of types.

    Used in tuple types: tuple[int, str, bool]

    Can only be used unpacked: type A[*P] = tuple[*P]
    """
    contents: list[ConcreteType]

    def name(self):
        return f"*[{', '.join(map(str, self.contents))}]"

    def unify_internal(self, other: "BaseType", mode: UnifyMode):
        from transpiler.phases.typing.exceptions import TypeMismatchError, TypeMismatchKind
        if type(other) != TypeTupleType:
            raise TypeMismatchError(self, other, TypeMismatchKind.DIFFERENT_TYPE)
        if len(self.contents) != len(other.contents):
            raise TypeMismatchError(self, other, TypeMismatchKind.DIFFERENT_TYPE)
        for a, b in zip(self.contents, other.contents):
            a.unify(b, mode)

@dataclass(unsafe_hash=False)
class TypeListType(ConcreteType):
    """
    Special type used to represent a list of types.

    Used in function types for the parameters: Callable[[int, int], int]
    """
    contents: list[ConcreteType]

    def name(self):
        return f"[{', '.join(map(str, self.contents))}]"

    def unify_internal(self, other: "BaseType", mode: UnifyMode):
        from transpiler.phases.typing.exceptions import TypeMismatchError, TypeMismatchKind
        if type(other) != TypeListType:
            raise TypeMismatchError(self, other, TypeMismatchKind.DIFFERENT_TYPE)
        if len(self.contents) != len(other.contents):
            raise TypeMismatchError(self, other, TypeMismatchKind.DIFFERENT_TYPE)
        for a, b in zip(self.contents, other.contents):
            a.unify(b, mode)

    def contains_internal(self, other: "BaseType") -> bool:
        return self == other or any(a.contains(other) for a in self.contents)

@dataclass(eq=False)
class UnionInstanceType(GenericInstanceType):
    types: list[ConcreteType]

    def try_assign_internal(self, other: BaseType) -> bool:
        return super().try_assign_internal(other) or any(t for t in self.types if t.try_assign(other))

class UnionType(UniqueTypeMixin, GenericType):
    def name(self):
        return "Union"

    def _instantiate(self, args: list[ConcreteType]) -> GenericInstanceType:
        return UnionInstanceType(args)

TY_UNION = UnionType()

class OptionalType(UniqueTypeMixin, GenericType):
    def name(self) -> str:
        return "Optional"

    def _instantiate(self, args: list[ConcreteType]) -> GenericInstanceType:
        assert len(args) == 1
        return UnionInstanceType([args[0], TY_NONE])

TY_OPTIONAL = OptionalType()

@typing.runtime_checkable
class MethodType(typing.Protocol):
    def remove_self(self, self_type) -> ...:
        raise NotImplementedError()

@dataclass(eq=False)
class CallableInstanceType(GenericInstanceType, MethodType):
    parameters: list[ConcreteType]
    return_type: ConcreteType
    optional_at: int = None
    is_variadic: bool = False
    is_native: bool = False

    def __post_init__(self):
        if self.optional_at is None and self.parameters is not None:
            self.optional_at = len(self.parameters)
        if not hasattr(self, "generic_args") and self.parameters is not None:
            self.generic_args = [*self.parameters, self.return_type]
        if not hasattr(self, "generic_parent"):
            self.generic_parent = None

    def remove_self(self, self_type):
        assert self.parameters[0].try_assign(self_type)
        res = dataclasses.replace(
            self,
            parameters=self.parameters[1:],
            optional_at=self.optional_at - 1
        )
        res.block_data = self.block_data
        return res

    def __str__(self):
        return f"({", ".join(map(str, self.parameters + (["*args"] if self.is_variadic else [])))}) -> {self.return_type}"

    def try_assign_internal(self, other: BaseType) -> bool:
        other = other.deref()
        if not isinstance(other, CallableInstanceType):
            return False

        self.unify(other)
        return True

# @dataclass(eq=False)
# class UserFunctionInstance(CallableInstanceType):
#     scope: "transpiler.phases.typing.scope.Scope" = None
#     node: ast.FunctionDef = None

class CallableType(UniqueTypeMixin, GenericType):
    def name(self):
        return "Callable"

    def _instantiate(self, args: list[ConcreteType]) -> CallableInstanceType:
        match args:
            case [TypeListType([*args]), ret]:
                return CallableInstanceType(args, ret)
            case _:
                raise ValueError

@dataclass(eq=False, init=False)
class LambdaInstanceType(CallableInstanceType):
    def __str__(self):
        return f"<lambda>({", ".join(map(str, self.parameters))}) -> {self.return_type}"

class LambdaType(CallableType):
    def name(self):
        return "<lambda>"

    def _instantiate(self, args: list[ConcreteType]) -> CallableInstanceType:
        match args:
            case [TypeListType([*args]), ret]:
                return CallableInstanceType(args, ret)
            case _:
                raise ValueError

TY_LAMBDA = LambdaType()

class BuiltinFeatureType(BuiltinType):
    @abstractmethod
    def feature(self):
        pass

    def __eq__(self, other):
        return type(self) == type(other)

def make_builtin_feature(name: str):
    match name:
        case "Optional":
            return TY_OPTIONAL
        case "Union":
            return TY_UNION
        case "Callable":
            return TY_CALLABLE
        case _:
            class CreatedType(BuiltinFeatureType):
                def name(self):
                    return name

                def feature(self):
                    return name
            CreatedType.__name__ = f"BuiltinFeatureType${name}"
            return CreatedType()

def make_cpp_type(name: str):
    class CreatedType(BuiltinType):
        def name(self):
            return name
    CreatedType.__name__ = f"CppTypeType${name}"
    return CreatedType()



TY_BUILTIN_FEATURE = create_builtin_generic_type("BuiltinFeature")
TY_CPP_TYPE = create_builtin_type("CppType")



TY_CALLABLE = CallableType()

@dataclass(eq=False)
class ClassTypeType(GenericInstanceType):
    inner_type: BaseType

class ClassType(UniqueTypeMixin, GenericType):
    parameters = [gparam("T")]

    def name(self):
        return "Type"

    def _instantiate(self, args: list[ConcreteType]) -> ClassTypeType:
        return ClassTypeType(*args)

TY_TYPE = ClassType()
