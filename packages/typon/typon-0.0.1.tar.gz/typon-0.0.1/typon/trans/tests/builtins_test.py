# coding: utf-8

from typon import is_cpp
import sys as sis
from sys import stdout as truc

# foo = 123
# test = (2 + 3) * 4
# glob = 5

# def g():
#     a = 8
#     if True:
#         b = 9
#         if True:
#             c = 10
#             if True:
#                 d = a + b + c
#     if True:
#         e = d + 1
#     print(e)

# def f(x):
#     return x + 1
#
#
# def fct(param: int):
#     loc = f(456)
#     global glob
#     loc = 789
#     glob = 123
#
# def fct2():
#     global glob
#     glob += 5


if __name__ == "__main__":
    print("is c++:", is_cpp())
    # TODO: doesn't compile under G++ 12.2, fixed in trunk on March 15
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=98056
    sum = 0
    for i in range(15):
        sum = sum + i
    # a = [n for n in range(10)]
    # b = [x for x in a if x % 2 == 0]
    #c = [y * y for y in b]
    print("C++   " if is_cpp() else "Python",
          "res=", 5, ".", True, [4, 5, 6],
          #{7, 8, 9},
    #       #[1, 2] + [3, 4], [5, 6] * 3,
                 #{1: 7, 9: 3},
           0x55 & 7 == 5,
    #       #3j,
          sum,
    #       # a,
    #       # b
          )
    print("Typon")
    print()
