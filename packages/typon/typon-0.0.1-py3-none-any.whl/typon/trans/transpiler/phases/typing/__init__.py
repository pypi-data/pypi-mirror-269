from transpiler.phases.typing.common import PRELUDE
from transpiler.phases.typing.scope import VarKind, VarDecl
from transpiler.phases.typing.types import TY_TASK, TY_CALLABLE, TY_OPTIONAL, TY_CPP_TYPE, TY_BUILTIN_FEATURE, TY_TUPLE, \
    TY_DICT, TY_SET, TY_LIST, TY_COMPLEX, TY_BYTES, TY_STR, TY_FLOAT, TY_INT, TY_BOOL, TY_OBJECT, TY_JOIN, TY_FUTURE, \
    TY_FORKED, TY_GENERATOR, TY_MUTEX, TY_SLICE

prelude_vars = {
    "object": TY_OBJECT,
    "bool": TY_BOOL,
    "int": TY_INT,
    "float": TY_FLOAT,
    "str": TY_STR,
    "bytes": TY_BYTES,
    "complex": TY_COMPLEX,
    "list": TY_LIST,
    "set": TY_SET,
    "dict": TY_DICT,
    "tuple": TY_TUPLE,
    "slice": TY_SLICE,
    "BuiltinFeature": TY_BUILTIN_FEATURE,
    "CppType": TY_CPP_TYPE,
    "Task": TY_TASK,
    "Join": TY_JOIN,
    "Future": TY_FUTURE,
    "Forked": TY_FORKED,
    "Generator": TY_GENERATOR,
    "Mutex": TY_MUTEX
}

PRELUDE.vars.update({name: VarDecl(VarKind.LOCAL, ty.type_type()) for name, ty in prelude_vars.items()})

