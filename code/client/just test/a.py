from queue import Queue
from threading import Thread


def add(x, y, q):
    result = x + y
    q.put(result)


q = Queue()
t = Thread(target=add, args=(3, 4, q))
t.start()
t.join()
result = q.get()
print(result)
