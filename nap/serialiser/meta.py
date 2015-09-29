from __future__ import unicode_literals

from django.utils.six import with_metaclass


class DeclarativeMetaclass(type):
    '''
    Mangle a class so any properties defined on it are stashed in _defaults
    '''
    def __new__(mcs, name, bases, attrs):
        defaults = {
            key: attrs.pop(key)
            for key in list(attrs.keys())
            if not key.startswith('_')
        }
        new_class = super(DeclarativeMetaclass, mcs).__new__(mcs, name, bases,
                                                             attrs)
        new_class._defaults = defaults
        return new_class


class Meta(with_metaclass(DeclarativeMetaclass, object)):
    '''Generic container for Meta classes'''

    def __init__(self, meta):
        ''' Copy value values onto ourself '''
        for key in dir(meta):
            if key.startswith('_'):
                continue
            if key not in self._defaults:
                raise ValueError('Property "%s" not supported by %s' % (key, self.__class__.__name__))
        for key, value in self._defaults.items():
            setattr(self, key, getattr(meta, key, value))
