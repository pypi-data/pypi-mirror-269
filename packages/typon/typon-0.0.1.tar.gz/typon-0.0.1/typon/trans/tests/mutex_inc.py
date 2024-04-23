from time import sleep

def inc(cell):
    x = cell.val
    sleep(1)
    cell.val = x + 1
    # todo: why doesnt it crash with a wrong field name ???
    print("current:", cell.val)

class Thing:
    x: int
    def __init__(self, x: int):
        self.x = x

    def inc(self):
        x = self.x
        sleep(1)
        self.x = x + 1
        print("current:", self.x)

def truc():
    m = Mutex(0)
    for _ in range(10):
        fork(lambda: m.when(inc))
    #sync()

def nomutex():
    t = Thing(0)
    for _ in range(10):
        fork(lambda: t.inc())
    #sync()


if __name__ == "__main__":
    print("Mutex:")
    truc()
    print("No mutex:")
    nomutex()
