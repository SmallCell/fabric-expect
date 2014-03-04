from __future__ import with_statement


class spawn (object):
    """This is the main class interface for expect.
    Use this class to start and control child channel.
    """

    def expect(self, timeout, *pattern):
        print pattern
        