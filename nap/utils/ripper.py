from collections import namedtuple
from operator import attrgetter


class Ripper:
    '''
    Extremely light-weight serialiser for very simple cases.

    See http://musings.tinbrain.net/blog/2015/aug/14/serialiser-hurry/ for
    details.
    '''
    def __init__(self, *args, **kwargs):
        for arg in args:
            kwargs.setdefault(arg, arg)
        self.getter = attrgetter(*kwargs.values())
        self.tup = namedtuple('tup', kwargs.keys())

    def __call__(self, obj):
        return self.tup._make(self.getter(obj))._asdict()
