from typing import Self, Protocol, Optional

assert 5

class object:
    def __eq__[T](self, other: T) -> bool: ...
    def __ne__[T](self, other: T) -> bool: ...

class int:
    def __add__(self, other: Self) -> Self: ...

    def __sub__(self, other: Self) -> Self: ...

    def __mul__(self, other: Self) -> Self: ...

    def __and__(self, other: Self) -> Self: ...

    def __neg__(self) -> Self: ...
    def __init__[T](self, x: T) -> None: ...
    def __lt__(self, other: Self) -> bool: ...
    def __gt__(self, other: Self) -> bool: ...
    def __mod__(self, other: Self) -> Self: ...
    def __ge__(self, other: Self) -> bool: ...

class float:
    def __init__(self, x: object) -> None: ...

assert int.__add__
assert (5).__add__

class slice[Start, Stop, Step]:
    pass


class HasLen(Protocol):
    def __len__(self) -> int: ...

def len(x: HasLen) -> int:
    ...

class Iterator[U](Protocol):
    def __iter__(self) -> Self: ...

    def __next__(self) -> U: ...

class Iterable[U](Protocol):
    def __iter__(self) -> Iterator[U]: ...

class str:
    def find(self, sub: Self) -> int: ...
    def format(self, *args) -> Self: ...
    def encode(self, encoding: Self) -> Self: ... # TODO: bytes
    def decode(self, encoding: Self) -> Self: ...
    def __len__(self) -> int: ...
    def __add__(self, other: Self) -> Self: ...
    def __mul__(self, other: int) -> Self: ...
    def startswith(self, prefix: Self) -> bool: ...
    def __getitem__(self, item: int | slice) -> Self: ...
    def isspace(self) -> bool: ...
    def __contains__(self, item: Self) -> bool: ...

assert len("a")
assert not len(6)

class bytes:
    def decode(self, encoding: str) -> str: ...
    def __len__(self) -> int: ...

class list[U]:

    def __add__(self, other: Self) -> Self: ...

    def __mul__(self, other: int) -> Self: ...

    def __getitem__(self, index: int) -> U: ...
    def __setitem__(self, index: int, value: U) -> None: ...

    def pop(self, index: int = -1) -> U: ...
    def __iter__(self) -> Iterator[U]: ...
    def __len__(self) -> int: ...
    def append(self, value: U) -> None: ...
    def __contains__(self, item: U) -> bool: ...
    def __init__(self, it: Iterator[U]) -> None: ...

assert [1, 2].__iter__()
assert list[int].__iter__

class dict[U, V]:
    def __getitem__(self, key: U) -> V: ...
    def __setitem__(self, key: U, value: V) -> None: ...
    def __len__(self) -> int: ...


assert(len(["a"]))
#assert list.__getitem__
assert [].__getitem__
assert [4].__getitem__
assert [1, 2, 3].__getitem__(1)

class set[U]:
    def __len__(self) -> int: ...
    def __contains__(self, item: U) -> bool: ...


def iter[U](x: Iterable[U]) -> Iterator[U]:
    ...

assert iter

def next[U](it: Iterator[U], default: Optional[U] = None) -> U:
    ...
# what happens with multiple functions

assert iter(["1", "2"])

def identity[U](x: U) -> U:
    ...

assert identity(1)
assert identity("a")

def identity_2[U, V](x: U, y: V) -> tuple[U, V]:
    ...

assert list.__add__
assert list.__add__([5], [6])
assert list[int].__add__
assert identity_2(1, "a")
assert lambda x, y: identity_2(x, y)
assert lambda x: identity_2(x, x)

def print(*args) -> None: ...

assert print

def input(prompt: str = "") -> str:
    ...

def range(*args) -> Iterator[int]: ...

assert [].__add__
assert [6].__add__
assert [True].__add__
assert lambda x: [x].__add__



assert next(range(6), None)

class file:
    def read(self, size: int=0) -> Task[str]: ...
    def close(self) -> Task[None]: ...
    def __enter__(self) -> Self: ...
    def __exit__(self) -> Task[bool]: ...

def open(filename: str, mode: str) -> Task[file]: ...

def __test_opt(x: int, y: int = 5) -> int:
    ...

assert __test_opt
assert __test_opt(5)
assert __test_opt(5, 6)
assert not __test_opt(5, 6, 7)
assert not __test_opt()

class __test_type:
    def __init__(self) -> None: ...

    def test_opt(self, x: int, y: int = 5) -> int:
        ...

assert __test_type().test_opt(5)
assert __test_type().test_opt(5, 6)
assert not __test_type().test_opt(5, 6, 7)
assert not __test_type().test_opt()

def exit(code: int | None = None) -> None: ...

class Exception:
    def __init__(self, message: str) -> None: ...

assert next([])

from typing import Callable

class Task[T]:
    pass

class Join[T]:
    pass

class Forked[T]:
    def get(self) -> T: ...

class Future[T]:
    def get(self) -> Task[T]: ...


assert Forked[int].get

def fork[T](f: Callable[[], T]) -> Task[Forked[T]]:
    # stub
    class Res:
        get = f
    return Res

assert fork(lambda: 1).get

def future[T](f: Callable[[], T]) -> Task[Future[T]]:
    # stub
    class Res:
        get = f
    return Res


def sync() -> None:
    # stub
    pass

class Cell[T]:
    def __init__(self, val: T) -> None: ...

class Mutex[T]:
    def __init__(self, val: T) -> None: ...

    def when[R](self, f: Callable[[Cell[T]], R]) -> R:
        pass

assert Cell(123)
assert Cell("abc")
assert Mutex(True)