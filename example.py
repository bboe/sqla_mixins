#!/usr/bin/env python
from __future__ import unicode_literals
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Unicode
from sqlalchemy.orm import sessionmaker, scoped_session
from sqla_mixins import BasicBase, UserMixin

if sys.version_info < (3, 0):
    builtins = __import__('__builtin__')
else:
    import builtins


Base = declarative_base(cls=BasicBase)
Session = scoped_session(sessionmaker())

# Make session available to sqla_mixins
builtins._sqla_mixins_session = Session


class User(UserMixin, Base):
    first_name = Column(Unicode, nullable=False)
    last_name = Column(Unicode, nullable=False)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return 'User: {0}\nHashed Password: {1}\n'.format(self.username,
                                                          self._password)


def initialize(engine):
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)


def main():
    engine = create_engine('sqlite://', echo=False)
    initialize(engine)

    session = Session()

    # Create a user completely by constructor
    user0 = User(first_name='Bryce', last_name='Boe',
                 username='bboe', password='some_password')

    # Create a user partially by constructor
    user1 = User(first_name='Cookie', last_name='Monster')
    user1.username = 'cmonster'
    user1.password = 'cookiesareanalwaysfood'

    # Create a user completely by attribute assigment
    user2 = User()
    user2.first_name = 'Foo'
    user2.last_name = 'Bar'
    user2.username = 'fbar'
    user2.password = 'therehadtobeafoobarexample'

    # Add the users to the database
    session.add_all([user0, user1, user2])
    session.commit()

    # Demonstrate that all their passwords are encrypted
    for user in session.query(User).all():
        # Note that `password` is not a readable attribute. The hashed password
        # is stored in the database as the field `_password`.
        print(user)

    # Update one of the passwords
    user2.set_password('another_password')
    print('Note that the following password is different from the previous.')
    print(user2)

    # Verify a user's password
    cookie_attempts = ['cookiesareasometimesfood', 'cookiesareanalwaysfood']
    for password in cookie_attempts:
        if user1.verify_password(password):
            print('The password is `{0}`'.format(password))
        else:
            print('The password is not `{0}`'.format(password))

    # Fetch a user by id
    user3 = User.fetch_by_id(user1.id)
    assert(user1 == user3)


if __name__ == "__main__":
    main()
