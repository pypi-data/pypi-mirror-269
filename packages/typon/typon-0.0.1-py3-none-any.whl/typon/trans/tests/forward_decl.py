# coding: utf-8

# https://lab.nexedi.com/xavier_thompson/typon-snippets/blob/master/module/mymodule.cpp
def f():
    return 1 + g()

def g():
    return f()

class T:
    def f(self):
        return 1 + self.g()

    def g(self):
        return self.f()

if __name__ == "__main__":
    pass