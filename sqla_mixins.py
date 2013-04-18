import sys
from passlib.hash import pbkdf2_sha512
from sqlalchemy import Column, DateTime, String, Integer, Unicode, func
from sqlalchemy.ext.declarative import declared_attr

if sys.version_info < (3, 0):
    builtins = __import__('__builtin__')
else:
    import builtins

__version__ = '0.6'


class BasicBase(object):
    """A base sqlalchemy class that provides `id` and `created_at` fields."""
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now(),
                        index=True, nullable=False)

    @declared_attr
    def __tablename__(cls):
        """The table name will be the lowercase of the class name."""
        return cls.__name__.lower()

    @classmethod
    def fetch_by(cls, **kwargs):
        """Return a single object (or None) by the named attributes."""
        return cls.query_by(**kwargs).first()

    @classmethod
    def fetch_by_id(cls, element_id):
        """Return an object (or None) by its id."""
        return cls.query_by(id=int(element_id)).first()

    @classmethod
    def query_by(cls, **kwargs):
        """Return a query result for the named attributes."""
        if not hasattr(builtins, '_sqla_mixins_session'):
            raise Exception('__builtin__._sqla_mixins_session must be set to '
                            'your session class')
        session = builtins._sqla_mixins_session()
        return session.query(cls).filter_by(**kwargs)

    def clone(self, exclude=None, update=None):
        """Return a shallow-copy clone of the sqlalchemy object.

        Relationship objects are not copied, however foreign key assignments
        held by this object are copied shallowly.

        :param exclude: If provided, should be an iterable that contains the
            names attributes to exclude from the copy. The attributes
            `created_at` and `id` are always excluded.
        :param update: If provided, should be a mapping of attribute name, to
            the value that should be set.

        """
        # Prepare attribute exclusion set
        if not exclude:
            exclude = set()
        if not isinstance(exclude, set):
            exclude = set(exclude)
        exclude.update(('created_at', 'id'))
        # Build a mapping of attributes to values
        attrs = {x: getattr(self, x) for x in self.__mapper__.columns.keys()
                 if x not in exclude}
        if update:  # Update the mapping if necessary
            attrs.update(update)
        # Build and return the SQLA object
        return self.__class__(**attrs)

    def update(self, _ignore_order=False, **kwargs):
        """Update the named attributes.

        Return true when an attribute was changed, indicating that the object
        should be added to the session and committed.

        Setting _ignore_order to True indicates that attribute lists should be
        sorted before being compared. This is useful when updating relationship
        lists.
        """
        modified = False
        for attr, value in kwargs.items():
            self_value = getattr(self, attr)
            if _ignore_order and (isinstance(self_value, list) and
                                  isinstance(value, list)):
                if sorted(self_value) != sorted(value):
                    setattr(self, attr, value)
                    modified = True
            elif getattr(self, attr) != value:
                setattr(self, attr, value)
                modified = True
        return modified


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
