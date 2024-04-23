# coding: utf-8

def function1():
    r = function2()
    print("function1()")
    return r

def function2():
    print("function2")
    return class1()

class class1:
    def method1(self):
        print("class1::method1()")

class class2(class1):
    def method2(self):
        self.method1()
        print("class2::method2()")

class class3(class1):
    def method2(self):
        self.method1()
        print("class3::method2()")

class class4(class2, class3):
    def method3(self):
        self.method1()
        print("class4::method3()")

if __name__ == "__main__":
    print(">>> o1 = function1()")
    o1 = function1()

    print(">>> o1.method1()")
    o1.method1()

    print(">>> o2 = class2()")
    o2 = class2()

    print(">>> o2.method1()")
    o2.method1()

    print(">>> o2.method2()")
    o2.method2()

    print(">>> o3 = class3()")
    o3 = class3()

    print(">>> o3.method2()")
    o3.method2()

    print(">>> o4 = class4()")
    o4 = class4()

    print(">>> o4.method3()")
    o4.method3()

