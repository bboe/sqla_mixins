#!/usr/bin/env python
import os
import re
from setuptools import setup

readme = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
version = re.search("__version__ = '([^']+)'",
                    open('sqla_mixins.py').read()).group(1)

setup(name='sqla_mixins',
      author='Bryce Boe',
      author_email='bbzbryce@gmail.com',
      classifiers=['Intended Audience :: Developers',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Topic :: Database :: Front-Ends'],
      description=('A python module that contains a number of simple '
                   'declarative sqlalchemy mixins.'),
      install_requires=['passlib', 'sqlalchemy'],
      long_description=readme,
      py_modules=['sqla_mixins'],
      url='http://cs.ucsb.edu/~bboe',
      version=version
      )
