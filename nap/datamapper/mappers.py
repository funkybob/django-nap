
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
        Allow implicit patch using:

        >>> obj = data >> mapper
        '''
        return self._patch(other)

    def _reduce(self):
        '''
        Reduce our instance to its serialisable state.

        Returns a dict.
        '''
        return {
            name: getattr(self, name)
            for name in self._field_names
        }

    def _clean(self, data, full=True):
        '''
        Hook for finall pass validation.

        full indicates if this is an _apply (True) or _patch (False)
        Should update self._errors dict.
        '''
        return

    def _patch(self, data):
        '''
        Update an instance from supplied data.
        '''

        errors = defaultdict(list)

        for name in self._field_names:
            try:
                value = data[name]
            except KeyError:
                continue
            try:
                setattr(self, name, value)
            except ValidationError as e:
                errors[name].append(e)

        self._errors = dict(errors)

        # Allow a final pass of cleaning
        self._clean(data, full=False)

        if self._errors:
            raise ValidationError(self._errors)

        return self._obj

    def _apply(self, data):
        '''
        Update an instance from supplied data.

        All fields marked required=True MUST be provided.
        All fields omitted will have their default used, if provided.
        '''
        errors = defaultdict(list)

        for name in self._field_names:
            required = getattr(self._fields[name], 'required', True)
            default = getattr(self._fields[name], 'default', NOT_PROVIDED)

            try:
                value = data[name]
            except KeyError:
                if required:
                    if default is NOT_PROVIDED:
                        errors[name].append(
                            ValidationError('This field is required')
                        )
                        continue
                elif default is NOT_PROVIDED:
                    continue
                value = default
            try:
                setattr(self, name, value)
            except ValidationError as e:
                errors[name].append(e)

        self._errors = dict(errors)

        # Allow a final pass of cleaning
        self._clean(data, full=True)

        if self._errors:
            raise ValidationError(self._errors)

        return self._obj
