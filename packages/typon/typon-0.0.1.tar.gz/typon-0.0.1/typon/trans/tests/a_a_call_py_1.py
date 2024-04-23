# test numpy interop

from numpy import square
import math

if __name__ == "__main__":
    x = [1, 2, 3, 4]
    y: list[int] = square(x)
    print(x, y)
    f: int = math.factorial(5)
    print("5! =", f)