# sqla_mixins

A python module that contains a number of simple declarative sqlalchemy mixins.
Currently it supports two such mixins:

* BasicBase

  The BasicBase class can be used either as a mixin or simply as the base class
  for all of your sqlalchemy classes. This mixin automatically provides the
  tablename for the class, as well as two columns, `id` and `created_at`.

* UserMixin

  The UserMixin class is great for storring username and password information
  into a database. It provides automatic password salting and hashing through
  the recommended [PBKDF2](http://en.wikipedia.org/wiki/PBKDF2) key derivation
  function.


### Installation

The sqla_mixins module can be installed via:

    pip install sqla_mixins

The module has been tested to work both with python 2.7 and python 3.2. It
should work with python 2.6 and any newer versions of python.

### Usage

For example usage of this module, please see the
[example.py](/bboe/sqla_mixins/blob/master/example.py) file.
