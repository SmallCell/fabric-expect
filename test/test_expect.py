"""Main test class for fabric-expect"""
import unittest

from fabric.contrib.expect import *

class TestChannel(unittest.TestCase):

    def setUp(self):
        pass

    def test_ok(self):
        assert(True)
        
class TestLoopback(unittest.TestCase):

    def setUp(self):
        pass
        
