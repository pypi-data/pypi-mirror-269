# coding: utf-8



def f1():
    return f2()

def f2():
    return f3()

def f3():
    return 123

if __name__ == "__main__":
    print(f3())