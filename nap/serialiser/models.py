
from django.core.exceptions import ValidationError
from django.db.models.fields import NOT_PROVIDED
from django.db.models.manager import Manager
from django.utils.six import with_metaclass

from . import fields
from .base import MetaSerialiser, Serialiser
from .meta import Meta

FIELD_MAP = {}
# Auto-construct the field map
for f in dir(fields):
    cls = getattr(fields, f)
    try:
        if issubclass(cls, fields.Field):
            FIELD_MAP[f] = cls
    except TypeError:
        pass


class ModelMeta(Meta):
    model = None
    # Fields to include from the Model
    fields = []
    field_types = {}
    # Fields to exclude from the Model
    exclude = []
    # Fields from the model to flag as read-only
    read_only_fields = []

    # When restoring an object, which fields do we treat as m2m?
    related_fields = []
    # When we try to retrieve an instance, which fields do we use?
    key_fields = ('id',)
    # When restoring an object, which attrs do we not use
    ignored_fields = ()
    # When calling get_or_create, what do we pass as defaults?
    defaults = {}
    # Are there any deserialised fields we must pass to get_or_create defaults?
    core_fields = ()


class MetaModelSerialiser(MetaSerialiser):
    meta_class = ModelMeta

    def __new__(mcs, name, bases, attrs):

        new_class = super(MetaModelSerialiser, mcs).__new__(mcs, name, bases, attrs)

        include = getattr(new_class._meta, 'fields', [])
        exclude = getattr(new_class._meta, 'exclude', [])
        read_only = getattr(new_class._meta, 'read_only_fields', [])

        current_fields = new_class._fields.keys()

        model_fields = {}
        model = new_class._meta.model
        if model is not None:
            for field in model._meta.fields:
                # If we've got one, skip...
                if field.name in current_fields:
                    continue

                # If we have a whitelist, and it's not in it, skip
                if include and field.name not in include:
                    continue

                # If it's blacklisted, skip
                if field.name in exclude:
                    continue

                kwargs = {
                    'readonly': field.name in read_only,
                    'null': field.null,
                }
                if field.default is not NOT_PROVIDED:
                    kwargs['default'] = field.default

                try:
                    field_class = new_class._meta.field_types[field.name]
                except KeyError:
                    field_class = FIELD_MAP.get(field.__class__.__name__, fields.Field)
                model_fields[field.name] = field_class(**kwargs)

        new_class._fields.update(model_fields)

        return new_class


class ModelSerialiser(with_metaclass(MetaModelSerialiser, Serialiser)):

    def restore_object(self, obj, instance, **kwargs):
        if instance:
            for key, val in obj.items():
                setattr(instance, key, val)
        else:
            instance = self._meta.model(**obj)
        if kwargs.get('commit', True):
            instance.save()
        return instance


class ModelReadSerialiser(ModelSerialiser):
    '''
    A Serialiser that will only Read, not Create, an instance on inflate.

    Specify only the fields you intend to filter by.
    '''

    def restore_object(self, objdata, instance, **kwargs):
        try:
            return self._meta.model.objects.get(**objdata)
        except self._meta.model.DoesNotExist:
            raise ValidationError('%s with values %r does not exist.' % (
                self._meta.model.__name__,
                objdata,
            ))


class ModelCreateUpdateSerialiser(ModelSerialiser):

    '''
    A ModelSerialiser with the ability to create/update instances from data.
    '''

    def restore_object(self, objdata, instance, **kwargs):
        related = {
            key: objdata.pop(key)
            for key in self._meta.related_fields
        }

        if instance is None:
            lookup = {
                field: objdata[field]
                for field in self._meta.key_fields
            }
            defaults = dict(self._meta.defaults)
            for key in self._meta.core_fields:
                defaults[key] = objdata[key]
            instance, _ = self._meta.model.objects.get_or_create(
                defaults=defaults,
                **lookup
            )

        for key, value in objdata.items():
            if key in self._meta.ignored_fields:
                continue
            setattr(instance, key, value)

        instance.save()

        for key, value in related.items():
            getattr(instance, key).add(*value)

        return instance


def modelserialiser_factory(name, model, **kwargs):
    attrs = {
        'model': model,
    }
    for key in ['fields', 'exclude', 'read_only']:
        try:
            attrs[key] = kwargs[key]
        except KeyError:
            pass

    meta = type(str('Meta'), (object,), attrs)
    return type(ModelSerialiser)(str(name), (ModelSerialiser,), {'Meta': meta})


class ModelSerialiserField(fields.SerialiserField):
    def __init__(self, *args, **kwargs):
        if 'serialiser' not in kwargs:
            model = kwargs.pop('model')
            kwargs['serialiser'] = modelserialiser_factory(model.__name__ + 'Serialiser', model, **kwargs)()
        super(ModelSerialiserField, self).__init__(*args, **kwargs)


class ModelManySerialiserField(fields.ManySerialiserField):
    def __init__(self, *args, **kwargs):
        if 'serialiser' not in kwargs:
            model = kwargs.pop('model')
            kwargs['serialiser'] = modelserialiser_factory(model.__name__ + 'Serialiser', model, **kwargs)()
        super(ModelManySerialiserField, self).__init__(*args, **kwargs)

    def reduce(self, value, **kwargs):
        if isinstance(value, Manager):
            value = value.all()
        return super(ModelManySerialiserField, self).reduce(value, **kwargs)
