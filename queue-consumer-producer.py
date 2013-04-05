from Queue import Queue
from threading import Thread

# simplified version from http://www.blog.pythonlibrary.org/2012/08/01/python-concurrency-an-example-of-a-queue/
# see also:
# http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained
# http://docs.python.org/2/library/queue.html

q = Queue()

# consumer thread pops items from the queue
def consume():
    while True:
        item = q.get()
        print 'pop %d' % ( item)
        q.task_done()

t = Thread(target=consume)
t.daemon = True
t.start()

# producer thread
limit = 10
for item in range(limit):
    q.put(item)
    print '-- put %d' % (item)
    
q.join() # wait for the queue to be empty

# for some reason, some line breaks are sometimes missing when printing


