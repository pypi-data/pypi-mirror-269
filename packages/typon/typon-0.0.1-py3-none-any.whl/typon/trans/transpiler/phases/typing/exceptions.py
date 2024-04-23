import ast
import enum
from dataclasses import dataclass

from transpiler.utils import highlight
from transpiler.exceptions import CompileError
from transpiler.phases.typing.types import TypeVariable, BaseType


@dataclass
class UnresolvedTypeVariableError(CompileError):
    variable: TypeVariable

    def __str__(self) -> str:
        return f"Unresolved type variable: {self.variable}"

    def detail(self, last_node: ast.AST = None) -> str:
        if isinstance(last_node, (ast.Import, ast.ImportFrom)):
            return f"""
            This indicates the compiler was unable to infer the type of a function in a module.
            
            Currently, Typon cannot determine the type of Python functions imported from other modules, except
            for the standard library.
            As such, you need to give enough information to the compiler to infer the type of the function.
            
            For example:
                     ↓↓↓ this tells the compiler that {highlight('math.factorial')} returns an {highlight('int')}
                {highlight('res: int = math.factorial(5)')}"""
        return f"""
        This generally indicates the compiler was unable to infer the type of a variable or expression.
        A common fix is to add a type annotation to the variable or function.
        
        For example:
                     ↓↓↓ this tells the compiler that {highlight('x')} is an {highlight('int')}
            {highlight('def f(x: int):')}
        """


@dataclass
class RecursiveTypeUnificationError(CompileError):
    needle: BaseType
    haystack: BaseType

    def __str__(self) -> str:
        return f"Recursive type unification: {highlight(self.needle)} and {highlight(self.haystack)}"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This generally indicates a recursive type definition. Such types are not currently supported.
        
        For example:
            {highlight('T = tuple[T]')}
            
        In the current case, {highlight(self.haystack)} contains type {highlight(self.needle)}, but an attempt was made to
        unify them.
        """


class TypeMismatchKind(enum.Enum):
    NO_COMMON_PARENT = enum.auto()
    DIFFERENT_TYPE = enum.auto()


@dataclass
class TypeMismatchError(CompileError):
    expected: BaseType
    got: BaseType
    reason: TypeMismatchKind

    def __str__(self) -> str:
        return f"Type mismatch: expected {highlight(self.expected)}, got {highlight(self.got)}"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This generally indicates a type error.
        
        For example:
            {highlight('def f(x: int): ...')}
            {highlight('f("hello")')}
            
        In the current case, the compiler expected an expression of type {highlight(self.expected)}, but instead got
        an expression of type {highlight(self.got)}.
        """


@dataclass
class ArgumentCountMismatchError(CompileError):
    func: "CallableInstanceType"
    arguments: "list"

    def __str__(self) -> str:
        fcount = str(len(self.func.parameters))
        if self.func.is_variadic:
            fcount = f"at least {fcount}"

        return f"Argument count mismatch: expected {fcount}, got {len(self.arguments)}"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates missing or extraneous arguments in a function call or type instantiation.
        The called or instantiated signature was {highlight(self.func)}.
        
        Other examples:
            {highlight('def f(x: int): ...')}
            {highlight('f(1, 2)')}
        Here, the function {highlight('f')} expects one argument, but was called with two.
            
            {highlight('x: list[int, str]')}
        Here, the type {highlight('list')} expects one argument, but was instantiated with two.
        """


@dataclass
class ProtocolMismatchError(CompileError):
    value: BaseType
    protocol: BaseType
    reason: Exception | str

    def __str__(self) -> str:
        return f"Protocol mismatch: {str(self.value)} does not implement {str(self.protocol)}"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This generally indicates a type error.
        
        For example:
            {highlight('def f(x: Iterable[int]): ...')}
            {highlight('f("hello")')}
            
        In the current case, the compiler expected an expression whose type implements {highlight(self.protocol)}, but
        instead got an expression of type {highlight(self.value)}. 
        """


@dataclass
class NotCallableError(CompileError):
    value: BaseType

    def __str__(self) -> str:
        return f"Trying to call a non-function type: {highlight(self.value)}"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that an attempt was made to call an object that is not a function.
        
        For example:
            {highlight('x = 1')}
            {highlight('x()')}
        """


@dataclass
class MissingAttributeError(CompileError):
    value: BaseType
    attribute: str

    def __str__(self) -> str:
        return f"Missing attribute: {highlight(self.value)} has no attribute {highlight(self.attribute)}"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that an attempt was made to access an attribute that does not exist.
        
        For example:
            {highlight('x = 1')}
            {highlight('print(x.y)')}
        """


@dataclass
class UnknownNameError(CompileError):
    name: str

    def __str__(self) -> str:
        return f"Unknown name: {highlight(self.name)}"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that an attempt was made to access a name that does not exist.
        
        For example:
            {highlight('print(abcd)')}
        """

@dataclass
class UnknownModuleError(CompileError):
    name: str

    def __str__(self) -> str:
        return f"Unknown module: {highlight(self.name)}"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that an attempt was made to import a module that does not exist.
        
        For example:
            {highlight('import abcd')}
        """



@dataclass
class UnknownModuleMemberError(CompileError):
    module: str
    name: str

    def __str__(self) -> str:
        return f"Unknown module member: Module {highlight(self.module)} does not contain {highlight(self.name)}"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that an attempt was made to import 
        
        For example:
            {highlight('from math import abcd')}
        """

@dataclass
class InvalidUnpackCountError(CompileError):
    value: BaseType
    count: int

    def __str__(self) -> str:
        return f"Invalid unpack: {highlight(self.value)} cannot be unpacked into {self.count} variables"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that an attempt was made to unpack a value that cannot be unpacked into the given number of
        variables.
        
        For example:
            {highlight('a, b, c = 1, 2')}
        """

@dataclass
class InvalidUnpackError(CompileError):
    value: BaseType

    def __str__(self) -> str:
        return f"Invalid unpack: {highlight(self.value)} cannot be unpacked"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that an attempt was made to unpack a value that cannot be unpacked.
        
        For example:
            {highlight('a, b, c = 1')}
                   
        Moreover, currently typon only supports unpacking tuples.
        """

@dataclass
class NotIterableError(CompileError):
    value: BaseType

    def __str__(self) -> str:
        return f"Not iterable: {highlight(self.value)} is not iterable"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that an attempt was made to iterate over a value that is not iterable.
        
        For example:
            {highlight('for x in 1: ...')}
            
        Iterable types must implement the Python {highlight('Iterable')} protocol, which requires the presence of a
        {highlight('__iter__')} method.
        """

@dataclass
class NotIteratorError(CompileError):
    value: BaseType

    def __str__(self) -> str:
        return f"Not iterator: {highlight(self.value)} is not an iterator"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that an attempt was made to iterate over a value that is not an iterator.
        
        For example:
            {highlight('x = next(5)')}
            
        Iterator types must implement the Python {highlight('Iterator')} protocol, which requires the presence of a
        {highlight('__next__')} method.
        """

@dataclass
class OutsideFunctionError(CompileError):
    def __str__(self) -> str:
        return f"{highlight('return')} and {highlight('nonlocal')} cannot be used outside of a function"

    def detail(self, last_node: ast.AST = None) -> str:
        return ""

@dataclass
class OutsideLoopError(CompileError):
    def __str__(self) -> str:
        return f"{highlight('break')} and {highlight('continue')} can only be used inside a loop"

    def detail(self, last_node: ast.AST = None) -> str:
        return ""

@dataclass
class MissingReturnError(CompileError):
    node: ast.FunctionDef

    def __str__(self) -> str:
        return f"Missing return: not all code paths in {highlight(self.node)} return"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that a function is missing a {highlight('return')} statement in one or more of its code paths.
        
        For example:
            {highlight('def f(x: int):')}
            {highlight('    if x > 0:')}
            {highlight('        return 1')}
            {highlight('    # if x <= 0, the function returns nothing')}
        """

@dataclass
class InconsistentMroError(CompileError):
    bases: list[BaseType]

    def __str__(self) -> str:
        return f"Cannot create a consistent method resolution order (MRO) for bases {'\n'.join(map(highlight, self.bases))}"

    def detail(self, last_node: ast.AST = None) -> str:
        return f"""
        This indicates that a class has an inconsistent method resolution order (MRO).
        
        For example:
            {highlight('class A: pass')}
            {highlight('class B(A): pass')}
            {highlight('class C(B, A): pass')}
        """