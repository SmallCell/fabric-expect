import unittest

from mock import patch

from fabric.api import hosts
from fabric.contrib.expect import spawn

from loop import LoopSocket

from fabric.api import execute
from functools import wraps

def execute_wrap(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        return execute( f, *args, **kwds )
    return wrapper

class TestSpawn(unittest.TestCase):
    
    def setUp(self):
        self.socks = LoopSocket()
        print ">> setup"
        pass

    def test_readlines(self):
        chan = spawn(self.socks)
        effects_iter = chan.readlines(5)

        for e in effects_iter:
            print ">> " + e

            
    def _test_expectations(self):
        print ">> expect"
        
        with patch.object(expect.spawn, 'readlines', side_effect=["1", "2", "3", ""]):
            thing = expect.spawn(self.socks)
            thing.expect(5,  {
                expect.EOF : lambda: self.assertEqual(False),
                expect.TIMEOUT : lambda: self.assertEqual(True),
                "*assword" : None
           })                
        
        
if __name__ == "__main__":
    unittest.main()

    