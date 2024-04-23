from time import sleep

class Actor[T]:
    mutex: Mutex[T]

    def __init__(self, val: T):
        self.mutex = Mutex(val)

    def when[U](self, f: Callable[[Cell[T]], U]):
        return future(lambda: self.mutex.when(f))

def inc(cell):
    #print("inc")
    x = cell.val
    sleep(1)
    cell.val = x + 1
    print("current:", cell.val)

def truc():
    a = Actor(0)
    for i in range(10):
        a.when(inc)
    future = a.when(lambda cell: print("final:", cell.val))
    future.get()
    print("done")

if __name__ == "__main__":
    print("Actor:")
    truc()