# coding: utf-8
from typing import Self


class stat_result:
    st_mode: int
    st_ino: int
    st_dev: int
    st_nlink: int
    st_uid: int
    st_gid: int
    st_size: int
    st_atime: float
    st_mtime: float
    st_ctime: float
    st_blocks: int
    st_blksize: int
    st_rdev: int
    st_flags: int
    st_gen: int
    st_birthtime: float

class DirEntry:
    name: str
    path: str

class _ScandirIterator:
    def __enter__(self) -> Self: ...
    def __exit__(self) -> bool: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> DirEntry: ...

def scandir(path: str = ".") -> _ScandirIterator: ...

def fsdecode(filename: str) -> str: ...

def stat(path: str) -> Task[stat_result]: ...

def readlink(path: str) -> str: ...