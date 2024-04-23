# coding: utf-8
# https://lab.nexedi.com/xavier_thompson/typon-snippets/tree/master/references
class Person:
    name: str
    age: int

    def __init__(self, name, age):
        print("init")
        self.name = name
        self.age = age

    def afficher(self):
        print("afficher", self.name, self.age)

def creer():
    return Person("jean", 123)

if __name__ == "__main__":
    y = Person
    x = creer()
    print("name", x.name)
    print("age", x.age)
    x.afficher()
    y.afficher(x)

