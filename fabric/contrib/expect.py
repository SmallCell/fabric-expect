from __future__ import with_statement

import sys, types, re
from fabric.state import env
from fabric.utils import (
    _pty_size,    
    )
from fabric.thread_handling import ThreadHandler
from StringIO import StringIO
from fabric.io import output_loop
import time
from fabric.network import ssh

class EOF(Exception):
    """Raised when EOF is read from a child. This usually means the child has exited."""

class TIMEOUT(Exception):
    """Raised when a read time exceeds the timeout. """

class spawn (object):
    """This is the main class interface for expect.
    Use this class to start and control child channel.
    """
    def __init__(self, channel, command = None, 
                 stdout=None, stderr=None, timeout=None):
        # timeout is for interact thread
        self.channel = channel
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr
        self.timeout = env.command_timeout if (timeout is None) else timeout

        self.channel.set_combine_stderr(True)

        rows, cols = _pty_size()
        channel.get_pty(width=cols, height=rows)

        channel.invoke_shell()
        if command:
            channel.sendall(command + "\n")

        self.stdout_buf, self.stderr_buf = [], []

        
    def expect(self, timeout, pattern):


        line = self.out_stream.read(80)
        print "$$" + line 
        self.stdout.write(line)
                
                
        print self.out_stream
            

    def readline(self, timeout):
        side_effect=["1", "2", "3", ""]
        for e in side_effect:
            yield e
        
    def send(self, message):
        print ">> s: " + message
        self.channel.sendall(message)

    def interact(self):
        pass

    def close(self):
        # Obtain exit code of remote program now that we're done.
        status = self.channel.recv_exit_status()
                
        # Wait for threads to exit so we aren't left with stale threads
        for worker in self.workers:
            worker.thread.join()
            worker.raise_if_needed()

        self.channel.close()
        
        self.out_stream.close()
        return status
        

    def compile_pattern_list(self, patterns):
        if patterns is None:
            return []
        if type(patterns) is not types.ListType:
            patterns = [patterns]

        compile_flags = re.DOTALL # Allow dot to match \n
        if self.ignorecase:
            compile_flags = compile_flags | re.IGNORECASE
        compiled_pattern_list = []
        for p in patterns:
            if type(p) in types.StringTypes:
                compiled_pattern_list.append(re.compile(p, compile_flags))
            elif p is EOF:
                compiled_pattern_list.append(EOF)
            elif p is TIMEOUT:
                compiled_pattern_list.append(TIMEOUT)
            elif type(p) is type(re.compile('')):
                compiled_pattern_list.append(p)
            else:
                raise TypeError ('Argument must be one of StringTypes, EOF, TIMEOUT, SRE_Pattern, or a list of those type. %s' % str(type(p)))

        return compiled_pattern_list
        