# class Cell[T]:
#     val: T
#
# class Mutex[T]:
#     cell: Cell[T]
#
#     def when[R](self, f: Callable[[Cell[T]], R]) -> R:
#         pass
#
#     def __enter__(self) -> Cell[T]:
#         # locks then returns cell
#         return self.cell
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         # unlocks
#         pass

# @arc
class Actor[T]:
    mutex: Mutex[T]

    def __init__(self, val: T):
        self.mutex = Mutex(val)

    # def when(self, f: Callable[[T], object]):
    #     return future(lambda: self.mutex.when(f))

def thing(x):
    print("hello", x)

if __name__ == "__main__":
    act = Actor(123)
    act.mutex.when(thing)

# class Actor[T]:
#     def __init__(self):
#         self.fifo = []
#         future(lambda: self.handle())
#
#     def handle(self):
#         while True:
#             if self.fifo:
#                 f = self.fifo.pop(0)
#                 self.mutex.when(f)
#             else:
#                 yield
#
#     mutex: Mutex[T]
#
#     def when(self, f: Callable[[T], object]):
#         #return future(lambda: self.mutex.when(f))
#         self.fifo.append(f)
#
#
#
# class A:
#     def f(self): pass
#
# a = Actor[A]()
#
# a.when(A.f)
#
# b = Actor[int]()

