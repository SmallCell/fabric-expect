from __future__ import with_statement

import sys, re
import socket
import time

from fabric.state import env
from fabric.utils import _pty_size
from fabric.thread_handling import ThreadHandler
from fabric.io import output_loop, input_loop
from fabric.context_managers import char_buffered
from fabric.network import ssh

class EOF(Exception):
    """Raised when EOF is read from a child. This usually means the child has exited."""

class TIMEOUT(Exception):
    """Raised when a read time exceeds the timeout. """

class spawn (object):
    """
    This is the main class interface for expect.
    Use this class to start and control child channel.
    """
    def __init__(self, channel, command = None,
                 stdout=None, stderr=None, timeout=None):
        # timeout is for interact thread
        self.channel = channel
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr
        self.timeout = env.command_timeout if (timeout is None) else timeout

        self.last_line = None
        self.last_match = None
        
        self.channel.set_combine_stderr(True)

        rows, cols = _pty_size()
        channel.get_pty(width=cols, height=rows)
        channel.settimeout(timeout)

        channel.invoke_shell()
        if command:
            channel.sendall(command + "\n")

        # switch to file IO
        self.fd = self.channel.makefile('rwb')

    def expect(self, timeout, pattern):
        """
        Read lines from input channel and match them against patterns.
        Execute matching action.
        When EOF or TIMEOUT are among the handlers excute it's action
        otherwise propaagate original exception. 
        """
        default_timeout = self.channel.gettimeout()
        self.channel.settimeout(timeout)
        matchers = filter(lambda e: not e in [EOF, TIMEOUT], pattern)
        self.last_match = None
        
        while(True):
            try:
                line = self.readline()
                mm = self.search(line, matchers)
                if mm:
                    pattern[mm] and pattern[mm]()
                    break
            except EOF, ex:
                if EOF in pattern.keys():
                    pattern[EOF] and pattern[EOF]()
                    break
                else:
                    raise ex
            except TIMEOUT, ex:
                if TIMEOUT in pattern.keys():
                    pattern[TIMEOUT] and pattern[TIMEOUT]()
                    break
                else:
                    raise ex
            finally:
                self.channel.settimeout(default_timeout)
                    
    def search(self, txt, expressions):
        """
        String matcher against list of regexp's
        """
        for m in expressions:
            res = re.match(m, txt)
            if res:
                self.last_match = m
                return self.last_match
        return None
        
    def readline(self):
        try:
            self.last_line = self.fd.readline()
            if self.fd.closed or len(self.last_line) == 0:
                raise EOF()                
        except socket.timeout:
            raise TIMEOUT()
            
        return self.last_line

    def send(self, message):
        self.fd.write(message)

    def interact(self):
        """
        Invoke shell interactive mode
        """
        with char_buffered(sys.stdin):
            # Init stdout, stderr capturing. Must use lists instead of strings as
            # strings are immutable and we're using these as pass-by-reference
            stdout_buf, stderr_buf = [], []
            workers = (
                ThreadHandler('out', output_loop, self.channel, "recv",
                              capture=stdout_buf, stream=self.stdout, timeout=self.timeout),
                ThreadHandler('err', output_loop, self.channel, "recv_stderr",
                              capture=stderr_buf, stream=self.stderr, timeout=self.timeout),
                ThreadHandler('in', input_loop, self.channel, True)
            )

            while True:
                if self.channel.exit_status_ready():
                    break
                else:
                    # Check for thread exceptions here so we can raise ASAP
                    # (without chance of getting blocked by, or hidden by an
                    # exception within, recv_exit_status())
                    for worker in workers:
                        worker.raise_if_needed()
                try:
                    time.sleep(ssh.io_sleep)
                except KeyboardInterrupt, e:
                    raise e

            # Obtain exit code of remote program now that we're done.
            status = self.channel.recv_exit_status()

            # Wait for threads to exit so we aren't left with stale threads
            for worker in workers:
                worker.thread.join()
                worker.raise_if_needed()

            # Close channel
            self.channel.close()

            return stdout_buf, stderr_buf, status
  
    def close(self):
        self.channel.close()
        self.channel.get_transport().close()

