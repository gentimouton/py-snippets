from Queue import Queue
from threading import Thread

# simplified version from http://www.blog.pythonlibrary.org/2012/08/01/python-concurrency-an-example-of-a-queue/
# see also:
# http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained
# http://docs.python.org/2/library/queue.html

# using multiprocessing: see https://gist.github.com/brantfaircloth/1255715

q = Queue(maxsize=10)

# consumer thread pops items from the queue
def consume():
    while True:
        item = q.get()
        q.task_done()

num_consumers = 7
for i in range(num_consumers):
    t = Thread(target=consume)
    t.daemon = True
    t.start()

# producer thread
limit = 10 ** 8
for item in range(limit):
    q.put(item)

q.join() # wait for the queue to be empty

# for some reason, some line breaks are sometimes missing when printing
