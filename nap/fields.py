
class Field(object):
    def __init__(self, attribute=None, default=None, *args, **kwargs):
        self.attribute = attribute
        self.default = default
        self.args = args
        self.kwargs = kwargs

    def deflate(self, name, obj, data):
        src = self.attribute
        if src is None:
            src = name
        data[name] = getattr(obj, src, self.default)

    def inflate(self, name, data, kwargs):
        dest = self.attribute
        if dest is None:
            dest = name
        try:
            kwargs[dest] = data[name]
        except KeyError:
            pass

