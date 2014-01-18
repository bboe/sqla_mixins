#!/usr/bin/env python
import os
import re
from setuptools import setup

MODULE_NAME = 'sqla_mixins'


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as fp:
    README = fp.read()
with open('{0}.py'.format(MODULE_NAME)) as fp:
    VERSION = re.search("__version__ = '([^']+)'", fp.read()).group(1)

setup(name=MODULE_NAME,
      author='Bryce Boe',
      author_email='bbzbryce@gmail.com',
      classifiers=['Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Topic :: Database :: Front-Ends'],
      description=('A python module that contains a number of simple '
                   'declarative sqlalchemy mixins.'),
      install_requires=['passlib>=1.6', 'sqlalchemy>=0.6.5'],
      license='Simplified BSD License',
      long_description=README,
      py_modules=[MODULE_NAME],
      url='https://github.com/bboe/sqla_mixins',
      version=VERSION)
