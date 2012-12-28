
from .fields import Field

class MetaSerialiser(type):
    def __new__(cls, name, bases, attrs):
        # Inherited fields
        attrs['_fields'] = {}

        # Inherit from parents
        parents = [b for b in bases if isinstance(b, Serialiser)]
        parents.reverse()

        for p in parents:
            parent_fields = getattr(p, '_fields', {})

            for name, field in parent_fields.items():
                attrs['_fields'][name] = field

        declared_fields = {}
        for name, field in attrs.items():
            if isinstnance(field, Field):
                declared_fields[name] = attrs.pop(name)

        attrs['_fields'].update(declared_fields)

        new_class = super(MetaSerialiser, cls).__new__(cls, name, bases, attrs

        return new_class

class Serialiser(object):
    __metaclass__ = MetaSerialiser


    def deflate_object(self, obj):
        data = {}
        for name, field in self._fields.items():
            field.deflate(name, obj, data)
            method = getattr(self, 'deflate_%s' % name, None)
            if method is not None:
                method(obj, data)
        return data

    def deflate_list(self, obj_list):
        for obj in iter(obj_list):
            yield self.serialise_object(obj)

    def build_instance(kwargs):
        '''Take the inflated data and create a new instance'''
        return self.obj_class(**kwargs)

    def inflate_object(self, data):
        kwargs = {}
        for name, field in self._fields.items():
            field.inflate(name, data, kwargs)
            method = getattr(self, 'inflate_%s' % name, None)
            if method is not None:
                method(data, kwargs)

        return self.build_instance(kwargs)

    def inflate_list(self, data_list):
        for data in data_list:
            yield self.inflate_object(data)

