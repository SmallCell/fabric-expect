Overview
========
How to answer to prompts automatically with python fabric?

Installation
============

fabric-expect is installed easily.

::

    easy_install fabric-expect

or

::

    pip install fabric-expect

    tox
    
    
Usage
=====

1. make your working procedure
1. execute it by fabric

::

     with open_interact_channel('sh') as chan:
         chan.expect(
             { 'timeout' : lambda: send_user("\nFailed to get password prompt\n") and exit(1),
               'eof'     : lambda send_user "\nSSH failure for $hostname\n" and exit 1,
               "*assword" : None
           })
     
         chan.send "$password\r"
     
         chan.expect({
             'timeout' : lambda: send_user "\nLogin failed. Password incorrect.\n" and  exit 1,
             "*\> " : None
         }
     
     )

    chan.interact()



Changelog
=========

0.0.1 (Tue Mar  4 14:47:11 EET 2014)
------------------
- First release


Travis
======

Travis CI - Distributed build platform for the open source community 

