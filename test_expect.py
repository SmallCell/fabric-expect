from __future__ import with_statement
"""Main test class for fabric-expect"""

# import time, sys
import unittest
# from fabric.network import ssh
# from loop import LoopSocket
# from fabric.io import output_loop
# from fabric.thread_handling import ThreadHandler
from fabric.state import default_channel
from fabric.api import run, env
from  fabric.contrib.expect import spawn, EOF, TIMEOUT

from fabric.api import execute
from functools import wraps

def execute_wrap(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        return execute( f, *args, **kwds )
    return wrapper

#@hosts('vkinzers@tauron:22')
           
class TestChannel(unittest.TestCase):

    def setUp(self):
        env.hosts = ["localhost"]
        pass
        # self.socks = LoopSocket()
        # self.sockc = LoopSocket()
        # self.socks.link(self.sockc)
        # self.sockc.link(self.socks)

    def tearDown(self):        
        # self.sockc.close()
        # self.socks.close()
        pass


    @execute_wrap
    def _test_channel(self):
        chan = spawn(default_channel(), '/bin/sh') 
        chan.send('ls')
        fd = chan.channel.makefile()
        res = fd.readline() 
        while len(res):
            print ">>" + res
            print ">>" + str(len(res))
            res = fd.readline()
         
    @execute_wrap
    def _test_hello_world(self):        
        run("echo 'Hello, Super Fabric!'")
        
    @execute_wrap
    def test_expect(self):
#        chan = spawn(self.socks)
        run("echo 'BEGIN'")
        chan = spawn(default_channel())
        chan.expect(5,  {
            EOF : lambda: chan.close(),
            TIMEOUT : lambda: self.assertEqual(False, "TIMEOUT"),
            'Last' : None
        })

        chan.send('uname -a\n')
        
        chan.expect(1,  {
            EOF : lambda: chan.close(),
            TIMEOUT : lambda: self.assertEqual(False, "TIMEOUT1"),
            'Linux' : None,
        })


#        chan.interact()
        
        chan.close()

        
#     def _test_spawn(self):
#         chan = spawn(self.sockc, 'sh')
#         res = self.socks.recv(10)
#         print ">> " + res
        
#         assert(res[:2] == 'sh')

#         self.socks.send("password")
#         chan.expect(3, {
#             "timeout" : lambda: chan.send("timeout"),
#             "EOF" : lambda: chan.close(),
#             ".*assword" : lambda: chan.send('valid'),
#         })
        
# #        res = self.socks.recv(10)
#         assert(res[:5] == 'valid')
        
        
if __name__ == "__main__":
    unittest.main()

"""        
class TestLoopback(unittest.TestCase):

    def setUp(self):
        pass


class TestSclish(unittest.TestCase):
    
    def setUp(self):
        self.socks = LoopSocket()
        self.sockc = LoopSocket()
        self.socks.link(self.sockc)
        self.sockc.link(self.socks)
        pass

    def _test_hello(self):
        self.socks.send("Hello")
        res = self.sockc.recv(10)
        print ">>" + res
        # self.socks.close()
        # self.sockc.close()
        pass

    def _test_thread_worker(self):
        stdout_buf = ""
        stdout_stream = sys.stdout
        workers = (
            ThreadHandler('out', output_loop, self.sockc, "recv",
                          capture=stdout_buf, stream=stdout_stream, timeout=2),
        )
#        import pdb; pdb.set_trace()

        self.socks.send("Hello\n")
        self.socks.send("World\n")
        
        time.sleep(ssh.io_sleep)
        
        self.socks.send("EOF")
        
#        self.sockc.close()
        self.socks.close()
        
        for worker in workers:
            worker.raise_if_needed()
        
        for worker in workers:
            worker.thread.join()
            worker.raise_if_needed()

"""        