
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

    def inflate_object(self, data, obj=None):
        if obj is None:
            # For now, we create a dummy object to hold the values
            obj = object()
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

class MetaModelSerialiser(MetaSerialiser):
    def __new__(cls, name, bases, attrs):

        include = attrs.pop('_fields', [])
        exclude = attrs.pop('_exclude', [])

        new_class = super(MetaModelSerialiser, cls).__new__(cls, name, bases, attrs)

        current_fields = new_class._fields.keys()

        try:
            for f in new_class._class._meta.fields:
                # If we've got one, skip...
                if f.name in current_fields:
                    continue

                # If we have a whitelist, and it's not in it, skip
                if include and not f.name in include:
                    continue

                # If it's blacklisted, skip
                if f.name in exclude:
                    continue

                kwargs = {
                    'default': f.default,
                }

                new_class._fields[f.name] = Field(**kwargs)
        except AttributeError:
            pass

        return new_class

class ModelSerialiser(Serialiser):
    __metaclass__ = MetaModelSerialiser

    # XXX How to create a new instance?
