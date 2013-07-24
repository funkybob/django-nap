from __future__ import unicode_literals

class Meta(object):
    '''Generic container for Meta classes'''

    def __new__(cls, meta=None):
        # Return a new class base on ourselves
        attrs = dict(
            (name, getattr(meta, name))
            for name in dir(meta)
            if not name[0] == '_'
        )
        return object.__new__(type(str('Meta'), (cls,), attrs))
