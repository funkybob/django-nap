
from inspect import classify_class_attrs

from django.core.exceptions import ValidationError
from django.db.models.fields import NOT_PROVIDED

from .fields import field
from .utils import DictObject


class MetaMapper(type):

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)

        new_fields = {
            name: prop
            for name, kind, cls, prop in classify_class_attrs(new_class)
            if isinstance(prop, field)
        }

        # Make sure we don't forget fields defined on parents
        fields = dict(bases[0]._fields) if bases else {}
        fields.update(new_fields)

        new_class._fields = fields
        new_class._field_names = tuple(fields.keys())

        return new_class


class Mapper(metaclass=MetaMapper):
    '''
    Mapper class.

    Provides a proxy class for retrieving and updating attributes on your
    objects.
    '''
    def __init__(self, obj=None, **kwargs):
        '''
        :param: obj Optionally bind to object
        :param: **kwargs Extra context (stored as self._context)
        '''
        if obj is None:
            obj = DictObject()
        self._obj = obj
        self._context = kwargs

    def __lshift__(self, other):
        '''
        Allow implicit reduction using:

        >>> data = mapper << obj
        '''
        self._obj = other
        return self._reduce()

    def __rrshift__(self, other):
        '''
        Allow implicit patch using:

        >>> obj = data >> mapper
        '''
        self._patch(other)
        return self._obj

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

        self._errors = errors = {}

        for name in self._field_names:
            if self._fields[name].readonly:
                continue
            try:
                value = data[name]
            except KeyError:
                continue
            try:
                setattr(self, name, value)
            except ValidationError as e:
                errors.setdefault(name, []).append(e)

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
        self._errors = errors = {}

        for name in self._field_names:
            if self._fields[name].readonly:
                continue

            required = self._fields[name].required
            default = self._fields[name].default

            try:
                value = data[name]
            except KeyError:
                if required:
                    if default is NOT_PROVIDED:
                        errors.setdefault(name, []).append(
                            ValidationError('This field is required')
                        )
                        continue
                elif default is NOT_PROVIDED:
                    continue
                value = default
                if callable(value):
                    value = value()
            try:
                setattr(self, name, value)
            except ValidationError as e:
                errors.setdefault(name, []).append(e)

        # Allow a final pass of cleaning
        self._clean(data, full=True)

        if self._errors:
            raise ValidationError(self._errors)

        return self._obj
