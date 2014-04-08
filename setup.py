from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import fabric.contrib.expect

version = '0.0.1'


here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)
    
setup(
    name='fabric-expect',
    version=version,
    description='How to answer to prompts automatically with python fabric',
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        #'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.7',
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Clustering",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
    ],
    author='ibnHatab',
    author_email='callistoiv+pypi@gmail.com',
    url='https://github.com/SmallCell/fabric-expect',
    license='BSD',
    cmdclass={'test': PyTest},
    test_suite='test.test_expect',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['fabric','fabric.contrib'],
    include_package_data=True,
    zip_safe=False,
    tests_require=['nose', 'mock', 'coverage'],
    install_requires=[
        # -*- Extra requirements: -*-
        'fabric',
    ],
     extras_require={
        'testing': ['pytest'],
    }
    
)
