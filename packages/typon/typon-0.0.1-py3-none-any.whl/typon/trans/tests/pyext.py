# coding: utf-8
# extension

from typon import export
import numpy as np
# from dataclasses import dataclass

# @dataclass
# class Person:
#     name: str
#     age: int
#
#     def afficher(self, msg: str):
#         print(msg, ",", self.name, self.age)
#         return 123

@export([int, int])
def add(x, y):
    return x + y

@export([int])
def fibo(n):
    res = [0, 1]
    for i in range(2, n):
        res.append(res[i - 1] + res[i - 2])
    return res

@export([])
def squares() -> list[int]:
    return np.square([x for x in range(5)])

if __name__ == "__main__":
    # p = Person("jean", 123)
    print("Python:", add(5, 3), fibo(10), squares())
    # p.afficher("Bonjour")