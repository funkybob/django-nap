from collections import namedtuple
from operator import attrgetter


class Ripper:
    '''
    Extremely light-weight serialiser for very simple cases.

    See https://blog.tinbrain.net/blog/serialiser-hurry.html for details.
    '''
    def __init__(self, *args, **kwargs):
        for arg in args:
            kwargs.setdefault(arg, arg)
        self.getter = attrgetter(*kwargs.values())
        self.tup = namedtuple('tup', kwargs.keys())

    def __call__(self, obj):
        return self.tup._make(self.getter(obj))._asdict()
