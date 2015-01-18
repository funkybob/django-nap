
from collections import defaultdict
from inspect import classify_class_attrs

from django.core.exceptions import ValidationError
from django.db.models.fields import NOT_PROVIDED
from django.utils.functional import cached_property

from .fields import field
from .utils import DictObject


class DataMapper(object):
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

    def __lshift__(self, other):
        '''
        Allow implicit reduction using:

        >>> data = mapper << obj
        '''
        self._obj = other
        return self._reduce()

    def __rlshift__(self, other):
        '''
        Allow implicit apply using:

        >>> obj = data >> mapper
        '''
        return self._apply(other)

    def _reduce(self):
        '''
        Reduce our instance to its serialisable state.

        Returns a dict.
        '''
        return {
            name: getattr(self, name)
            for name in self._field_names
        }

    def _apply(self, data, full=False):
        '''
        Update an instance from supplied data.

        If full is True, all fields not tagged as .required=False MUST be
        supplied in the data dict.
        '''
        errors = defaultdict(list)

        for name in self._field_names:
            required = getattr(self._fields[name], 'required', True)
            default = getattr(self._fields[name], 'default', NOT_PROVIDED)
            value = data.get(name, default)
            if value is NOT_PROVIDED:
                if full and required:
                    errors[name].append(
                        ValidationError('This field is required')
                    )
                continue
            try:
                setattr(self, name, value)
            except ValidationError as e:
                errors[name].append(e.message)

        self._errors = dict(errors)
        if errors:
            raise ValidationError(self._errors)

        return self._obj
