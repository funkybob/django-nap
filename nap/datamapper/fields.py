
from django.db.models.fields import NOT_PROVIDED
from django.forms import ValidationError

from nap.utils import digattr


class field(property):
    '''A base class to compare against.'''
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
    class V(DataView):
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


class ViewField(Field):
    def __init__(self, *args, **kwargs):
        self.view = kwargs.pop('view')
        super(ViewField, self).__init__(*args, **kwargs)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        value = super(ViewField, self).__get__(instance, cls)
        view = self.view()
        return view << value

    def __set__(self, instance, value):
        view = self.view(instance)
        view._update(value, update=True)
