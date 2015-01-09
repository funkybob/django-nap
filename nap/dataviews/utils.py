
class DictObject(dict):
    '''
    Provides a JavaScript-esque Object where attribute access is
    equivalent to dict access.

    >>> a = DictObject()
    >>> a['a'] = 1
    >>> a.a
    1
    >>> a.a = 3
    >>> a['a']
    3
    '''
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('%s object has no attribute %s' % (self, key))

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]
