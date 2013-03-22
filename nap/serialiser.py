
from . import fields
from .meta import Meta


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

    def object_deflate(self, obj, **kwargs):
        data = {}
        for name, field in self._fields.items():
            field.deflate(name, obj=obj, data=data, **kwargs)
            method = getattr(self, 'deflate_%s' % name, None)
            if method is not None:
                data[name] = method(obj=obj, data=data, **kwargs)
        return data

    def list_deflate(self, obj_list, **kwargs):
        return [
            self.object_deflate(obj, **kwargs)
            for obj in iter(obj_list)
        ]

    def object_inflate(self, data, instance=None, **kwargs):
        obj = {}
        for name, field in self._fields.items():
            if field.readonly:
                continue
            method = getattr(self, 'inflate_%s' % name, None)
            if method is not None:
                obj[name] = method(data=data, obj=obj, instance=instance, **kwargs)
            else:
                field.inflate(name, data, obj, **kwargs)
        return self.restore_object(obj, instance=instance, **kwargs)

    def list_inflate(self, data_list, **kwargs):
        # XXX target object list?
        return [
            self.object_inflate(data, **kwargs)
            for data in data_list
        ]

    def restore_object(self, obj, **kwargs): # pragma: no cover
        raise NotImplementedError
