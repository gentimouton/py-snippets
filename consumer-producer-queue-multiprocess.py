from multiprocessing import Process, JoinableQueue
import time

# using multiprocessing: see https://gist.github.com/brantfaircloth/1255715
# and https://gist.github.com/brantfaircloth/260331#file-gistfile1-py

q = JoinableQueue(maxsize=10)

# consumer thread pops items from the queue
def consume():
    print 'start consumer'
    while True:
        item = q.get()
        q.task_done()

# launch consumers
num_consumers = 7
for i in range(num_consumers):
    p = Process(target=consume)
    p.daemon = True
    p.start()

start = time.time()

# producer thread
num_items = 10 ** 5
print 'start producer'
for item in range(num_items):
    q.put(item)
print 'producer done'


q.join() # wait for the queue to be empty
q.close()

print '%d consumers took %f seconds' % (num_consumers, time.time() - start)

# for some reason, some line breaks are sometimes missing when printing
