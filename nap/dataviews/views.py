
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
    def _fields(self):
        return {
            name: prop
            for name, kind, cls, prop in classify_class_attrs(self.__class__)
            if isinstance(prop, field)
        }

    @cached_property
    def _field_names(self):
        return tuple(self._fields.keys())

    def _reduce(self):
        '''
        Reduce our instance to its serialisable state.

        Returns a dict.
        '''
        return {
            name: getattr(self, name)
            for name in self._field_names
        }

    def _apply(self, data, update=False):
        '''
        Update an instance from supplied data.

        If update is False, all fields not tagged as ._required=False MUST be
        supplied in the data dict.
        '''
        errors = defaultdict(list)
        for name in self._field_names:
            try:
                setattr(self, name, data[name])
            except KeyError:
                if self.update:
                    pass
                if getattr(self._fields[name], '_required', True):
                    errors[name].append(
                        ValidationError('This field is required')
                    )
            except ValidationError as e:
                errors[name].append(e.message)

        self._errors = dict(errors)
        if errors:
            raise ValidationError(self._errors)

        return self._obj
