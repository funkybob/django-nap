
from collections import defaultdict
from inspect import classify_class_attrs

from django.forms import ValidationError
from django.utils.functional import cached_property

from .fields import field
from .utils import DictObject


class DataView(object):
    def __init__(self, obj=None, **kwargs):

        if obj is None:
            obj = DictObject()
        self._obj = obj
        self._kwargs = kwargs

    @cached_property
    def _field_names(self):
        return tuple(
            name
            for name, kind, cls, prop in classify_class_attrs(self.__class__)
            if isinstance(prop, field)
        )

    def _reduce(self):
        '''
        Reduce our instance to its serialisable state.

        Returns a dict.
        '''
        return {
            name: getattr(self, name)
            for name in self._field_names
        }

    def _update(self, data):
        '''
        Update an instance from supplied data.
        '''
        errors = defaultdict(list)
        for name in self._field_names:
            if name in data:
                try:
                    setattr(self, name, data[name])
                except ValidationError as e:
                    errors[name].append(e.message)
        self._errors = dict(errors)
        if errors:
            raise ValidationError(self._errors)

        return self._obj
