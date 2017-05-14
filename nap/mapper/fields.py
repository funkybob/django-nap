import datetime
from functools import partial

from django.db.models.fields import NOT_PROVIDED

from nap.utils import digattr


class field(property):
    '''A base class to compare against.'''
    def __new__(cls, *args, **kwargs):
        '''
        Allow specifying keyword arguments when used as a decorator.
        '''
        if not args:
            return partial(field, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.required = kwargs.pop('required', False)
        self.default = kwargs.pop('default', NOT_PROVIDED)
        self.readonly = kwargs.pop('readonly', False)
        super().__init__(*args, **kwargs)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self.fget(instance._obj)

    def __set__(self, instance, value):
        if self.fset is None:
            return
        self.fset(instance._obj, value)


class context_field(field):
    '''Special case of field that allows access to the Mapper itself'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = kwargs

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self.fget(self, instance._obj)

    def __set__(self, instance, value):
        if self.fset is None:
            return
        return self.fset(self, instance._obj, value)


class Field(field):
    def __init__(self, attr, *args, **kwargs):
        self.attr = attr
        super().__init__(*args, **kwargs)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        value = getattr(instance._obj, self.attr, self.default)
        return self.get(value)

    def __set__(self, instance, value):
        if self.readonly:
            raise AttributeError('Field {.name} is read-only.'.format(self))
        value = self.set(value)
        setattr(instance._obj, self.attr, value)

    def get(self, value):
        return value

    def set(self, value):
        return value


class BooleanField(Field):
    def set(self, value):
        if value is None:
            return value
        if isinstance(value, bool):
            return value
        return value.lower() in (1, '1', 't', 'y', 'true')


class IntegerField(Field):
    def get(self, value):
        return int(value)

    def set(self, value):
        return int(value)


class FloatField(Field):
    def get(self, value):
        return float(value)

    def set(self, value):
        return float(value)


class TimeField(Field):
    def get(self, value):
        if value is None:
            return value
        return value.replace(microsecond=0).isoformat()

    def set(self, value):
        if value is None or isinstance(value, datetime.time):
            return value
            return datetime.datetime.strptime(value, '%H:%M:%S').time()


class DateField(Field):
    def get(self, value):
        if value is None:
            return value
        return value.isoformat()

    def set(self, value):
        if value is None or isinstance(value, datetime.date):
            return value
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()


class DateTimeField(Field):
    def get(self, value):
        if value is None:
            return value
        return value.replace(microsecond=0).isoformat(' ')

    def set(self, value):
        if value is None or isinstance(value, datetime.datetime):
            return value
        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


class MapperField(Field):
    '''
    A field that passes data through a Mapper.

    Useful for handling nested models.
    '''
    def __init__(self, *args, **kwargs):
        self.mapper = kwargs.pop('mapper')
        super().__init__(*args, **kwargs)

    def get(self, value):
        return self.mapper() << value

    def set(self, value):
        return value >> self.mapper()


class DigField(Field):
    '''
    Use digattr to resolve values in a DTL compatible syntax.
    '''
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('readonly', True)
        super().__init__(*args, **kwargs)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return digattr(instance._obj, self.name, self.default)
