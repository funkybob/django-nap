
from .fields import Field

class MetaSerialiser(type):
    def __new__(cls, name, bases, attrs):
        # Inherited fields
        attrs['_fields'] = {}

        # Inherit from parents
        try:
            parents = [b for b in bases if issubclass(b, Serialiser)]
            parents = []
            parents.reverse()

            for p in parents:
                parent_fields = getattr(p, '_fields', {})

                for name, field in parent_fields.items():
                    attrs['_fields'][name] = field
        except NameError:
            # Can't do this for Serialiser
            pass

        declared_fields = {}
        for name, field in attrs.items():
            if isinstance(field, Field):
                declared_fields[name] = attrs.pop(name)

        attrs['_fields'].update(declared_fields)

        new_class = super(MetaSerialiser, cls).__new__(cls, name, bases, attrs)

        return new_class

class Serialiser(object):
    __metaclass__ = MetaSerialiser


    def deflate_object(self, obj):
        data = {}
        for name, field in self._fields.items():
            field.deflate(name, obj, data)
            method = getattr(self, 'deflate_%s' % name, None)
            if method is not None:
                data[name] = method(obj, data)
        return data

    def deflate_list(self, obj_list):
        return [
            self.deflate_object(obj)
            for obj in iter(obj_list)
        ]

    def build_instance(self, kwargs):
        '''Take the inflated data and create a new instance'''
        return self._class(**kwargs)

    def inflate_object(self, data, obj=None, extra=None):
        if obj is None:
            # XXX Still not sure about this
            if not extra:
                extra = {}
            obj = self.build_instance(extra)
        for name, field in self._fields.items():
            if field.readonly:
                continue
            method = getattr(self, 'inflate_%s' % name, None)
            if method is not None:
                method(data, obj)
            else:
                field.inflate(name, data, obj)
        return obj

    def inflate_list(self, data_list):
        return [
            self.inflate_object(data)
            for data in data_list
        ]
