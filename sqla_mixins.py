from passlib.hash import pbkdf2_sha512
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, DateTime, String, Integer, Unicode

__version__ = '0.1'


class BasicBase(object):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now(), index=True,
                        nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class UserMixin(object):
    HASH_ROUNDS = 12000
    SALT_SIZE = 16
    username = Column(Unicode, index=True, nullable=False, unique=True)
    _password = Column(String, nullable=False)

    @classmethod
    def hash_password(cls, password):
        return pbkdf2_sha512.encrypt(password, rounds=cls.HASH_ROUNDS,
                                     salt_size=cls.SALT_SIZE)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            kwargs['_password'] = UserMixin.hash_password(kwargs['password'])
            del kwargs['password']
        super(UserMixin, self).__init__(*args, **kwargs)

    def set_password(self, password):
        self._password = self.hash_password(password)
    password = property(fset=set_password)

    def verify_password(self, password):
        return pbkdf2_sha512.verify(password, self._password)
