
from django.db.models.fields import NOT_PROVIDED

from nap.utils import digattr


class field(property):
    '''A base class to compare against.'''
    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self.fget(instance._obj)

    def __set__(self, instance, value):
        self.fset(instance._obj, value)


class Field(field):
    '''
    class V(DataView):
        foo = Field('bar', default=1)
    '''
    def __init__(self, name, default=NOT_PROVIDED, filters=None):
        self.name = name
        self.default = default
        self.filters = filters or []

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        value = getattr(instance._obj, self.name, self.default)
        for filt in self.filters:
            value = filt.from_python(value)
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

    def __set__(self, instance):
        raise NotImplementedError
