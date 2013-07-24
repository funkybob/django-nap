from __future__ import unicode_literals

from . import fields
from .meta import Meta
from six import with_metaclass

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
        for field_name, field in list(attrs.items()):
            if isinstance(field, fields.Field):
                declared_fields[field_name] = attrs.pop(field_name)

        attrs['_fields'].update(declared_fields)

        new_class = super(MetaSerialiser, mcs).__new__(mcs, name, bases, attrs)
        meta = getattr(new_class, 'Meta', None)
        new_class._meta = Meta(meta)

        return new_class


class Serialiser(with_metaclass(MetaSerialiser,object)):
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
        obj = {}
        for name, method in self._field_inflaters:
            method(name, data=data, obj=obj, instance=instance, **kwargs)
        for name, method in self._custom_inflaters:
            obj[name] = method(data=data, obj=obj, instance=instance, **kwargs)
        return self.restore_object(obj, instance=instance, **kwargs)

    def list_inflate(self, data_list, **kwargs):
        # XXX target object list?
        return [
            self.object_inflate(data, **kwargs)
            for data in data_list
        ]

    def restore_object(self, obj, **kwargs): # pragma: no cover
        raise NotImplementedError
