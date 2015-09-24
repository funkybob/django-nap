from __future__ import unicode_literals

from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError

from ..utils import digattr

try:
    from django.utils.encoding import force_text
except ImportError:
    # For Django1.4
    from django.utils.encoding import force_unicode as force_text


class NoDefault(object):
    '''Indicates no default value was provided.'''


class Field(object):
    type_class = None

    def __init__(self, attribute=None, default=NoDefault, readonly=False,
                 null=True, virtual=False, **kwargs):
        self.attribute = attribute
        self.default = default
        self.readonly = readonly
        self.null = null
        self.virtual = virtual
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
        if value is NoDefault:
            if self.virtual:
                return
            raise AttributeError('No attribute "%s" found on %r' % (src, obj,))
        if value is not None:
            value = self.reduce(value, **kwargs)
        data[name] = value

    def inflate(self, name, data, obj, **kwargs):
        if self.readonly:
            return
        dest = self._get_attrname(name)
        try:
            value = data[name]
        except KeyError:
            if self.default is not NoDefault and 'instance' not in kwargs:
                obj[dest] = self.default
            return

        if value is not None:
            try:
                value = self.restore(value, **kwargs)
            except ValueError:
                raise ValidationError(
                    "Field '%s' (%r) received invalid value: %r" % (
                        name, self.__class__.__name__, value
                        )
                )
        elif not self.null:
            raise ValidationError("Field '%s' must not be None." % name)

        obj[dest] = value


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
        return value.replace(microsecond=0).isoformat(str(' '))

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

    def __init__(self, *args, **kwargs):
        super(SerialiserField, self).__init__(*args, **kwargs)
        self.serialiser = kwargs['serialiser']

    def reduce(self, value, **kwargs):
        return self.serialiser.object_deflate(value, **kwargs)

    def restore(self, value, **kwargs):
        return self.serialiser.object_inflate(value, **kwargs)


class ManySerialiserField(Field):

    def __init__(self, *args, **kwargs):
        super(ManySerialiserField, self).__init__(*args, **kwargs)
        self.serialiser = kwargs['serialiser']

    def reduce(self, value, **kwargs):
        return self.serialiser.list_deflate(value, **kwargs)

    def restore(self, value, **kwargs):
        return self.serialiser.list_inflate(value, **kwargs)


class FileField(Field):

    def reduce(self, value, **kwargs):
        return value.url

    def restore(self, value, **kwargs):
        pass


class StringField(Field):
    '''
    Like Field, but always casts value to a text type.

    Since it can't know what type to restore to, it is set readonly by
    default.  If you want it to be writable, you must clear this flag and
    provide a custom inflater.
    '''
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('readonly', True)
        super(StringField, self).__init__(*args, **kwargs)

    def reduce(self, value, **kwargs):
        return force_text(value)
