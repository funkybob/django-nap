
from .utils import digattr

from decimal import Decimal
from datetime import datetime

class Field(object):
    type_class = None

    def __init__(self, attribute=None, default=None, readonly=False,
        *args, **kwargs):
        self.attribute = attribute
        self.default = default
        self.readonly = readonly
        self.args = args
        self.kwargs = kwargs

    def _get_attrname(self, name):
        return self.attribute if self.attribute else name

    def reduce(self, value):
        return value
    def restore(self, value):
        if self.type_class is not None:
            return self.type_class(value)
        return value

    def deflate(self, name, obj, data, **kwargs):
        src = self._get_attrname(name)
        value = digattr(obj, src, self.default)
        if value is not None:
            value = self.reduce(value)
        data[name] = value

    def inflate(self, name, data, obj, **kwargs):
        if self.readonly:
            return
        dest = self._get_attrname(name)
        try:
            value = data[name]
            obj[dest] = self.restore(value)
        except KeyError:
            pass


class IntegerField(Field):
    type_class = int

class DecimalField(Field):
    type_class = Decimal
    def reduce(self, value):
        return float(value)


class DateTimeField(Field):
    def reduce(self, value):
        return value.replace(microsecond=0).isoformat(' ')
    def restore(self, value):
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


class DateField(Field):
    def reduce(self, value):
        return value.isoformat()
    def restore(self, value):
        return datetime.strptime(value, '%Y-%m-%d').date()


class TimeField(Field):
    def reduce(self, value):
        return value.isoformat()
    def restore(self, value):
        return datetime.strptime(value, '%H:%M:%S').time()


class SerialiserField(Field):
    def __init__(self, serialiser, *args, **kwargs):
        super(SerialiserField, self).__init__(*args, **kwargs)
        self.serialiser = serialiser

    def deflate(self, name, obj, data, **kwargs):
        src = self._get_attrname(name)
        val = digattr(obj, src, self.default)
        data[name] = self.serialiser.deflate_object(val)

    def inflate(self, name, data, obj, **kwargs):
        if self.readonly:
            return
        dest = self._get_attrname(name)
        try:
            obj[dest] = self.serialiser.inflate_object(data[name])
        except KeyError:
            pass


class ManySerialiserField(Field):
    def __init__(self, serialiser, *args, **kwargs):
        super(ManySerialiserField, self).__init__(*args, **kwargs)
        self.serialiser = serialiser

    def deflate(self, name, obj, data, **kwargs):
        src = self._get_attrname(name)
        val = digattr(obj, src, self.default)
        data[name] = self.serialiser.deflate_list(iter(val), **kwargs)

    def inflate(self, name, data, obj, **kwargs):
        if self.readonly:
            return
        dest = self._get_attrname(name)
        try:
            obj[dest] = self.serialiser.inflate_list(data[name], **kwargs)
        except KeyError:
            pass
