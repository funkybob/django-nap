
from .fields import Field
from .meta import Meta

class MetaSerialiser(type):
    def __new__(cls, name, bases, attrs):
        # Inherited fields
        attrs['_fields'] = {}

        # Inherit from parents
        try:
            parents = [b for b in bases if issubclass(b, Serialiser)]
            parents.reverse()

            for p in parents:
                parent_fields = getattr(p, '_fields', {})

                attrs['_fields'].update(parent_fields)
        except NameError:
            # Can't do this for Serialiser
            pass

        declared_fields = {}
        for field_name, field in attrs.items():
            if isinstance(field, Field):
                declared_fields[field_name] = attrs.pop(field_name)

        attrs['_fields'].update(declared_fields)

        new_class = super(MetaSerialiser, cls).__new__(cls, name, bases, attrs)
        meta = getattr(new_class, 'Meta', None)
        new_class._meta = Meta(meta)

        return new_class


class Serialiser(object):
    __metaclass__ = MetaSerialiser


    def deflate_object(self, obj, publisher=None):
        data = {}
        for name, field in self._fields.items():
            field.deflate(name, obj, data, publisher=publisher)
            method = getattr(self, 'deflate_%s' % name, None)
            if method is not None:
                data[name] = method(obj, data, publisher=publisher)
        return data

    def deflate_list(self, obj_list, publisher=None):
        return [
            self.deflate_object(obj, publisher=publisher)
            for obj in iter(obj_list)
        ]

    def inflate_object(self, data, obj=None, publisher=None):
        if obj is None:
            # For now, we create a dummy object to hold the values
            obj = object()
        for name, field in self._fields.items():
            if field.readonly:
                continue
            method = getattr(self, 'inflate_%s' % name, None)
            if method is not None:
                method(data, obj, publisher=publisher)
            else:
                field.inflate(name, data, obj, publisher=publisher)
        return obj

    def inflate_list(self, data_list):
        return [
            self.inflate_object(data)
            for data in data_list
        ]

class MetaModelSerialiser(MetaSerialiser):
    def __new__(cls, name, bases, attrs):

        new_class = super(MetaModelSerialiser, cls).__new__(cls, name, bases, attrs)

        include = getattr(new_class._meta, 'fields', [])
        exclude = getattr(new_class._meta, 'exclude', [])

        current_fields = new_class._fields.keys()

        try:
            model = new_class._meta.model
            for f in model._meta.fields:
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
