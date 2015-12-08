from functools import partial

from django.core.exceptions import ValidationError
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
        return super(field, cls).__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.required = kwargs.pop('required', False)
        self.default = kwargs.pop('default', NOT_PROVIDED)
        super(field, self).__init__(*args, **kwargs)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self.fget(instance._obj)

    def __set__(self, instance, value):
        if self.fset is None:
            return
        self.fset(instance._obj, value)


class Field(field):
    '''
    class V(DataMapper):
        foo = Field('bar', default=1)
    '''
    def __init__(self, name, default=NOT_PROVIDED, filters=None,
                 required=True):
        self.name = name
        self.default = default
        self.filters = filters or []
        self.required = required

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        value = getattr(instance._obj, self.name, self.default)
        for filt in self.filters:
            try:
                value = filt.from_python(value)
            except (TypeError, ValueError):
                raise ValidationError('Invalid value')
        return value

    def __set__(self, instance, value):
        for filt in self.filters[::-1]:
            value = filt.to_python(value)
        setattr(instance._obj, self.name, value)


class DigField(Field):

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return digattr(instance._obj, self.name, self.default)

    def __set__(self, instance, value):
        raise NotImplementedError


class MapperField(Field):
    def __init__(self, *args, **kwargs):
        self.mapper = kwargs.pop('mapper')
        super(MapperField, self).__init__(*args, **kwargs)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        value = super(MapperField, self).__get__(instance, cls)
        mapper = self.mapper()
        return mapper << value

    def __set__(self, instance, value):
        mapper = self.mapper(instance)
        mapper._update(value, update=True)
