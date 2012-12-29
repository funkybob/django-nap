
from .utils import digattr, undigattr

class Field(object):

    def __init__(self, attribute=None, default=None, readonly=False,
        *args, **kwargs):
        self.attribute = attribute
        self.default = default
        self.readonly = readonly
        self.args = args
        self.kwargs = kwargs

    def deflate(self, name, obj, data):
        src = self.attribute
        if src is None:
            src = name
        data[name] = digattr(obj, src, self.default)

    def inflate(self, name, data, obj):
        if self.readonly:
            return
        dest = self.attribute
        if dest is None:
            dest = name
        try:
            setattr(obj, dest, data[name])
        except KeyError:
            pass
