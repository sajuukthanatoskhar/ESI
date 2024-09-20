import threading
import _thread
from queue import Queue
import time

print_lock = threading.Lock()
queueumult = Queue()
def exampleJob(worker):
    time.sleep(0.5)
    with print_lock:
        print(threading.current_thread().name,worker)

def threader():
    while True:
        worker = queueumult.get()
        exampleJob(worker)
        queueumult.task_done()


def test1():
    for x in range(10):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()
    start = time.time()
    for worker in range(20):
        queueumult.put(worker)
    queueumult.join()
    print('Entire job took:' + str(time.time() - start))


if __name__ == '__main__':
    pass