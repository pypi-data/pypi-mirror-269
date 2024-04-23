def f[T](x: T):
    return x

def g[X](a: X, b: X):
    return a + b

class H:
    def h[X](self, x: X):
        return x

class Box[T]:
    val: T

    def __init__(self, val: T):
        self.val = val

if __name__ == "__main__":
    print(f("abc"))
    print(f(6))
    print(g(6, 8))
    print(g("abc", "def"))
    # print(g("abc", 213)) # expected error
    print(H().h(6))

    #Box(6)