# coding: utf-8

from typing import Self

AF_INET6: int
SOCK_STREAM: int
SOL_SOCKET: int
SO_REUSEADDR: int

class socket:
    def setsockopt(self, level: int, option: int, value: int) -> None:
        pass

    def bind(self, address: tuple[str, int] | str) -> None:
        pass

    def connect(self, address: tuple[str, int] | str) -> None:
        pass

    def listen(self, backlog: int) -> None:
        pass

    def accept(self) -> Task[tuple[Self, str]]:
        pass

    def recv(self, bufsize: int) -> Task[bytes]:
        pass

    def send(self, data: str) -> Task[None]:
        pass

    def __init__(self, family: int, type: int) -> Self:
        pass

    def close(self) -> Task[None]:
        pass

def getaddrinfo(host: str, port: int, family: int = 0, type: int = 0, proto: int = 0, flags: int = 0) -> \
        Task[list[tuple[int, int, int, str, str]]]: # todo: incomplete return type
    pass

AF_UNIX: int