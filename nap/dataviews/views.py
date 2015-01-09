
from inspect import classify_class_attrs

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

    def _restore(self, data):
        '''
        Restore data from reduced state to a full instance.
        '''
        for name in self._field_names:
            if name in data:
                setattr(self, name, data[name])
        return self._obj

    def _construct(self, data):
        '''
        Any follow up work required to turn our raised data into an instance.
        '''
        return self._obj
