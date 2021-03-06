"""
Simple JSON wrapper on top of asynchat TCP sockets. 
Provides on_open, on_close, on_msg, do_send, and do_close.

Public domain

With inspiration from:
http://pymotw.com/2/asynchat/
http://code.google.com/p/podsixnet/
http://docstore.mik.ua/orelly/other/python/0596001886_pythonian-chp-19-sect-3.html


#################
# Echo server:
#################
from network import Listener, Handler, poll

class MyHandler(Handler):
    def on_msg(self, data):
        self.do_send(data)
        
class EchoServer(Listener):
    handlerClass = MyHandler

server = EchoServer(8888)
while 1:
    poll()


#################
# One-message client:
#################
from network import Handler, poll

done = False

class Client(Handler):
    def on_open(self):
        self.do_send({'a': [1,2], 5: 'hi'})
        global done
        done = True

client = Client('localhost', 8888)
while not done:
    poll()
client.do_close()

"""

import asynchat
import asyncore
import json
import socket


class Handler(asynchat.async_chat):
    
    def __init__(self, host, port, sock=None):
        if sock:  # passive side: Handler automatically created by a Listener
            asynchat.async_chat.__init__(self, sock)
        else:  # active side: Handler created manually
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
            asynchat.async_chat.__init__(self, sock)
            self.connect((host, port))  # asynchronous and non-blocking
        self.set_terminator('\0')
        self._buffer = []
        
    def collect_incoming_data(self, data):
        self._buffer.append(data)

    def found_terminator(self):
        msg = json.loads(''.join(self._buffer))
        self._buffer = []
        self.on_msg(msg)
    
    def handle_close(self):
        self.close()
        self.on_close()

    def handle_connect(self):  # called on the active side
        self.on_open()
        
    # API you can use
    def do_send(self, msg):
        self.push(json.dumps(msg) + '\0')
        
    def do_close(self):
        self.handle_close()  # will call self.on_close
    
    # callbacks you should override
    def on_open(self):
        pass
        
    def on_close(self):
        pass
        
    def on_msg(self, data):
        pass
    
    
class Listener(asyncore.dispatcher):
    
    handlerClass = Handler
      
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
        self.bind(('', port))
        self.listen(5)  # max 5 incoming connections at once (Windows' limit)

    def handle_accept(self):  # called on the passive side
        sock, (host, port) = self.accept()
        h = self.handlerClass(host, port, sock)
        h.on_open()
    
    def stop(self):
        self.close()

    
def poll():
    asyncore.loop(timeout=0, count=1) # return right away
