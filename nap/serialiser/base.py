from __future__ import unicode_literals

import inspect
from collections import defaultdict

from django.core.exceptions import ValidationError
from django.utils.six import with_metaclass

from . import fields
from .meta import Meta


class MetaSerialiser(type):
    meta_class = Meta

    def __new__(mcs, name, bases, attrs):
        attrs['_fields'] = {}

        # Remove from attrs
        meta = attrs.pop('Meta', None)

        # Field declared on this new class
        declared_fields = {}
        for field_name, field in list(attrs.items()):
            if isinstance(field, fields.Field):
                declared_fields[field_name] = attrs.pop(field_name)

        new_class = super(MetaSerialiser, mcs).__new__(mcs, name, bases, attrs)

        # Find fields declared on parents
        base_fields = {}
        for base in reversed(inspect.getmro(new_class)):
            base_fields.update(getattr(base, '_fields', {}))

        base_fields.update(declared_fields)
        new_class._fields = base_fields

        # Handle class Meta
        new_class._meta = mcs.meta_class(meta)

        return new_class


class Serialiser(with_metaclass(MetaSerialiser, object)):
    obj_class = None

    def __init__(self):
        '''
        Since the list of methods to call to deflate/inflate an object
        don't change, we might as well construct the lists once right here.
        '''
        # Build list of deflate and inflate methods
        self._field_deflaters = []
        self._custom_deflaters = []
        self._field_inflaters = []
        self._custom_inflaters = []

        for name, field in self._fields.items():
            self._field_deflaters.append((name, field.deflate))
            method = getattr(self, 'deflate_%s' % name, None)
            if method is not None:
                self._custom_deflaters.append((name, method))

            if field.readonly:
                continue
            method = getattr(self, 'inflate_%s' % name, None)
            if method:
                self._custom_inflaters.append((name, method))
            else:
                self._field_inflaters.append((name, field.inflate))

    def object_deflate(self, obj, **kwargs):
        data = {}
        for name, method in self._field_deflaters:
            method(name, obj=obj, data=data, **kwargs)
        for name, method in self._custom_deflaters:
            data[name] = method(obj=obj, data=data, **kwargs)
        return data

    def list_deflate(self, obj_list, **kwargs):
        return [
            self.object_deflate(obj, **kwargs)
            for obj in iter(obj_list)
        ]

    def object_inflate(self, data, instance=None, **kwargs):
        objdata = {}
        errors = defaultdict(list)
        for name, method in self._field_inflaters:
            try:
                method(
                    name,
                    data=data,
                    obj=objdata,
                    instance=instance,
                    **kwargs
                )
            except ValidationError as exc:
                errors[name].append(exc)
        for name, method in self._custom_inflaters:
            try:
                objdata[name] = method(
                    data=data,
                    obj=objdata,
                    instance=instance,
                    **kwargs
                )
            except ValidationError as exc:
                errors[name].append(exc)
        if errors:
            raise ValidationError(errors)
        return self.restore_object(objdata, instance=instance, **kwargs)

    def list_inflate(self, data_list, **kwargs):
        # XXX target object list?
        return [
            self.object_inflate(data, **kwargs)
            for data in data_list
        ]

    def restore_object(self, objdata, **kwargs):  # pragma: no cover
        if not self.obj_class:
            raise NotImplementedError
        return self.obj_class(objdata)
