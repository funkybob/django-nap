
from .utils import digattr

from decimal import Decimal
from datetime import datetime

class Field(object):
    type_class = None

    def __init__(self, attribute=None, default=None, readonly=False,
        **kwargs):
        self.attribute = attribute
        self.default = default
        self.readonly = readonly
        self.kwargs = kwargs

    def _get_attrname(self, name):
        return self.attribute if self.attribute else name

    def reduce(self, value, **kwargs):
        return value
    def restore(self, value, **kwargs):
        if self.type_class is not None:
            return self.type_class(value)
        return value

    def deflate(self, name, obj, data, **kwargs):
        src = self._get_attrname(name)
        value = digattr(obj, src, self.default)
        if value is not None:
            value = self.reduce(value, **kwargs)
        data[name] = value

    def inflate(self, name, data, obj, **kwargs):
        if self.readonly:
            return
        dest = self._get_attrname(name)
        try:
            value = data[name]
            obj[dest] = self.restore(value, **kwargs)
        except KeyError:
            pass

class BooleanField(Field):
    type_class = bool

class IntegerField(Field):
    type_class = int

class DecimalField(Field):
    type_class = Decimal
    def reduce(self, value, **kwargs):
        return float(value)


class DateTimeField(Field):
    def reduce(self, value, **kwargs):
        return value.replace(microsecond=0).isoformat(' ')
    def restore(self, value, **kwargs):
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


class DateField(Field):
    def reduce(self, value, **kwargs):
        return value.isoformat()
    def restore(self, value, **kwargs):
        return datetime.strptime(value, '%Y-%m-%d').date()


class TimeField(Field):
    def reduce(self, value, **kwargs):
        return value.isoformat()
    def restore(self, value, **kwargs):
        return datetime.strptime(value, '%H:%M:%S').time()


class SerialiserField(Field):
    def __init__(self, **kwargs):
        super(SerialiserField, self).__init__(**kwargs)
        self.serialiser = kwargs['serialiser']

    def reduce(self, value, **kwargs):
        return self.serialiser.object_deflate(value)
    def restore(self, value, **kwargs):
        return self.serialiser.object_inflate(value)


class ManySerialiserField(Field):
    def __init__(self, *args, **kwargs):
        super(ManySerialiserField, self).__init__(*args, **kwargs)
        self.serialiser = kwargs['serialiser']

    def reduce(self, value, **kwargs):
        return self.serialiser.list_deflate(iter(value), **kwargs)
    def restore(self, value, **kwargs):
        return self.serialiser.list_inflate(value, **kwargs)


class FileField(Field):
    def reduce(self, value, **kwargs):
        return value.url
    def restore(self, value, **kwargs):
        pass
