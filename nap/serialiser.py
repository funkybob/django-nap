
from . import fields
from .meta import Meta

from functools import partial

class MetaSerialiser(type):
    def __new__(mcs, name, bases, attrs):
        # Inherited fields
        attrs['_fields'] = {}

        # Inherit from parents
        try:
            for base in bases[::-1]:
                parent_fields = getattr(base, '_fields', {})
                attrs['_fields'].update(parent_fields)
        except NameError:
            # Can't do this for Serialiser
            pass

        declared_fields = {}
        for field_name, field in attrs.items():
            if isinstance(field, fields.Field):
                declared_fields[field_name] = attrs.pop(field_name)

        attrs['_fields'].update(declared_fields)

        new_class = super(MetaSerialiser, mcs).__new__(mcs, name, bases, attrs)
        meta = getattr(new_class, 'Meta', None)
        new_class._meta = Meta(meta)

        return new_class


class Serialiser(object):
    __metaclass__ = MetaSerialiser

    def __init__(self):
        # Build list of deflate and inflate methods
        self._deflaters = []
        self._inflaters = []
        def _setter(name, method, obj, data, *args, **kwargs):
            '''Wrapper for deflate_FOO'''
            data[name] = method(obj=obj, data=data, *args, **kwargs)
        def _getter(name, method, data, obj, *args, **kwargs):
            obj[name] = method(data=data, obj=obj, *args, **kwargs)

        for name, field in self._fields.items():
            self._deflaters.append(partial(field.deflate, name))
            method = getattr(self, 'deflate_%s' % name, None)
            if method is not None:
                self._deflaters.append(partial(_setter, name, method))

            if field.readonly:
                continue
            method = getattr(self, 'inflate_%s' % name, None)
            if method:
                self._inflaters.append(partial(_getter, name, method))
            else:
                self._inflaters.append(partial(field.inflate, name))

    def object_deflate(self, obj, **kwargs):
        data = {}
        for method in self._deflaters:
            method(obj=obj, data=data, **kwargs)
        return data

    def list_deflate(self, obj_list, **kwargs):
        return [
            self.object_deflate(obj, **kwargs)
            for obj in iter(obj_list)
        ]

    def object_inflate(self, data, instance=None, **kwargs):
        obj = {}
        for method in self._inflaters:
            method(data=data, obj=obj, instance=instance, **kwargs)
        return self.restore_object(obj, instance=instance, **kwargs)

    def list_inflate(self, data_list, **kwargs):
        # XXX target object list?
        return [
            self.object_inflate(data, **kwargs)
            for data in data_list
        ]

    def restore_object(self, obj, **kwargs): # pragma: no cover
        raise NotImplementedError
