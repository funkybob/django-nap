import datetime
from functools import partial

from django.db.models.fields import NOT_PROVIDED


class field(property):
    '''A base class to compare against.'''
    def __new__(cls, *args, **kwargs):
        '''
        Allow specifying keyword arguments when used as a decorator.
        '''
        if not args:
            return partial(cls, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.required = kwargs.pop('required', False)
        self.default = kwargs.pop('default', NOT_PROVIDED)
        self.readonly = kwargs.pop('readonly', False)
        self.null = kwargs.pop('null', False)
        super().__init__(*args, **kwargs)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self.fget(instance._obj)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance._obj, value)

    def setter(self, func):
        kwargs = self.__dict__.copy()
        kwargs.pop('__doc__')
        return self.__class__(self.fget, func, **kwargs)


class context_field(field):
    '''Special case of field that allows access to the Mapper itself'''
    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self.fget(instance._obj, instance._context)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        return self.fset(instance._obj, value, instance._context)


class Field(field):
    def __init__(self, attr, *args, **kwargs):
        self.attr = attr
        super().__init__(*args, **kwargs)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        value = getattr(instance._obj, self.attr, self.default)
        if self.null and value is None:
            return value
        return self.get(value)

    def __set__(self, instance, value):
        if self.readonly:
            raise AttributeError('Field is read-only.')
        if value is None:
            if not self.null:
                raise ValueError('Field may not be None')
        else:
            value = self.set(value)
        setattr(instance._obj, self.attr, value)

    def get(self, value):
        return value

    def set(self, value):
        return value


class BooleanField(Field):
    def set(self, value):
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
        return value.replace(microsecond=0).isoformat()

    def set(self, value):
        if isinstance(value, datetime.time):
            return value
        return datetime.datetime.strptime(value, '%H:%M:%S').time()


class DateField(Field):
    def get(self, value):
        return value.isoformat()

    def set(self, value):
        if isinstance(value, datetime.date):
            return value
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()


class DateTimeField(Field):
    def get(self, value):
        return value.replace(microsecond=0).isoformat(' ')

    def set(self, value):
        if isinstance(value, datetime.datetime):
            return value
        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


class MapperField(Field):
    '''
    A field that passes data through a Mapper.
    '''
    def __init__(self, *args, **kwargs):
        self.mapper = kwargs.pop('mapper')
        super().__init__(*args, **kwargs)

    def get(self, value):
        return self.mapper() << value

    def set(self, value):
        return value >> self.mapper()
