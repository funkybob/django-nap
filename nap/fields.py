
from .utils import digattr, undigattr

class Field(object):

    def __init__(self, attribute=None, default=None, readonly=False,
        *args, **kwargs):
        self.attribute = attribute
        self.default = default
        self.readonly = readonly
        self.args = args
        self.kwargs = kwargs

    def _get_attrname(self, name):
        return self.attribute if self.attribute else name

    def deflate(self, name, obj, data, publisher=None):
        src = self._get_attrname(name)
        data[name] = digattr(obj, src, self.default)

    def inflate(self, name, data, obj, publisher=None):
        if self.readonly:
            return
        dest = self._get_attrname(name)
        try:
            setattr(obj, dest, data[name])
        except KeyError:
            pass

class SerialiserField(Field):
    def __init__(self, *args, **kwargs):
        super(SerialiserField, self).__init__(*args, **kwargs)
        self.serialiser = self.kwargs.pop('serialiser')

    def deflate(self, name, obj, data, publisher=None):
        src = self._get_attrname(name)
        val = digattr(obj, src, self.default)
        data[name] = self.serialiser.deflate_object(val)

    def inflate(self, name, obj, data, publisher=None):
        if self.readonly:
            return
        dest = self._get_attrname(name)
        try:
            val = self.serialiser.inflate_object(data[name])
        except KeyError:
            pass
        else:
           setattr(obj, dest, val)

class ManySerialiserField(Field):
    def __init__(self, *args, **kwargs):
        super(ManySerialiserField, self).__init__(*args, **kwargs)
        self.serialiser = self.kwargs.pop('serialiser')

    def deflate(self, name, obj, data, publisher=None):
        src = self._get_attrname(name)
        val = digattr(obj, src, self.default)
        data[name] = self.serialiser.deflate_list(iter(val), publisher=publisher)

    def inflate(self, name, obj, data, publisher=None):
        if self.readonly:
            return
        dest = self._get_attrname(name)
        try:
            val = self.serialiser.inflate_list(data[name], publisher=publisher)
        except KeyError:
            pass
        else:
            setattr(obj, dest, val)

