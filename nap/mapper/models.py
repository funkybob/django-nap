from django.core.exceptions import ValidationError
from django.db.models import Manager
from django.db.models.fields import NOT_PROVIDED
from django.db import transaction

from . import fields
from .base import Mapper, MetaMapper as BaseMetaMapper


class Options:
    def __init__(self, meta):
        self.model = getattr(meta, 'model', None)
        field_list = getattr(meta, 'fields', [])
        if field_list != '__all__':
            field_list = set(field_list)
        self.fields = field_list
        self.exclude = set(getattr(meta, 'exclude', []))
        self.required = getattr(meta, 'required', {})
        self.readonly = set(getattr(meta, 'readonly', []))


class MetaMapper(BaseMetaMapper):

    def __new__(mcs, name, bases, attrs):
        meta = Options(attrs.get('Meta', None))

        if meta.model is None:
            if name != 'ModelMapper':
                raise ValueError('No model defined on class Meta.')
        else:
            existing = attrs.copy()
            for base in reversed(bases):
                existing.update(base._fields)

            # for f in meta.model._meta.get_fields():
            for f in meta.model._meta.fields:
                # Don't auto-add fields defined on this class or our parents
                if f.name in existing:
                    continue
                if f.name in meta.exclude:
                    continue
                if meta.fields != '__all__' and \
                   f.name not in meta.fields:
                    # Ensure model validation is told to exclude this
                    meta.exclude.add(f.name)
                    continue

                # Magic for field types
                kwargs = {
                    'readonly': f.name in meta.readonly or not f.editable,
                    'required': meta.required.get(f.name, not f.blank),
                    'null': f.null,
                }
                if f.null and getattr(f, 'default', NOT_PROVIDED) is NOT_PROVIDED:
                    kwargs['default'] = None
                else:
                    kwargs['default'] = f.default

                if f.is_relation:
                    kwargs['model'] = f.related_model
                    # OneToOneField or ForeignKey
                    if f.one_to_one or f.many_to_one:
                        field_class = ToOneField
                    # M2M on this model
                    elif f.many_to_many and not f.auto_created:
                        field_class = ToManyField
                else:
                    field_class = FIELD_MAP.get(f.__class__.__name__, fields.Field)

                attrs[f.name] = field_class(f.name, **kwargs)
            # Inherit
            attrs = dict(existing, **attrs)
        attrs['_meta'] = meta

        return super().__new__(mcs, name, bases, attrs)


class ModelMapper(Mapper, metaclass=MetaMapper):

    def __init__(self, obj=None, **kwargs):
        if obj is None:
            obj = self._meta.model()
        super().__init__(obj, **kwargs)

    def __irshift__(self, other):
        '''
        Allow implicit "update new instance" using:

        >>> obj = data >>= mapper
        '''
        self.obj = self._meta.model()
        return self._apply(other)

    def _clean(self, data, full=True):
        try:
            self._obj.full_clean(exclude=self._meta.exclude)
        except ValidationError as e:
            for k, v in e.message_dict.items():
                self._errors.setdefault(k, []).extend(v)


class RelatedField(fields.Field):
    mapper = None

    def __init__(self, *args, model=None, mapper=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.related_model = model
        self.mapper = mapper


class ToOneField(RelatedField):

    def get(self, value):
        if self.mapper:
            return self.mapper(value)._reduce()
        if value is None:
            return value
        return value.pk

    def set(self, value):
        if self.mapper:
            return self.mapper() << value
        return self.related_model.objects.get(pk=value)


class ToManyField(RelatedField):

    def get(self, value):
        if isinstance(value, Manager):
            value = value.all()
        if self.mapper:
            m = self.mapper()
            return [m << obj for obj in iter(value)]
        return [obj.pk for obj in iter(value)]

    def __set__(self, instance, value):
        if self.readonly:
            raise AttributeError('Field is read-only.')
        if value is None:
            if not self.null:
                raise ValueError('Field may not be None')
        else:
            value = self.set(value)
        with transaction.atomic():
            getattr(instance._obj, self.attr).set(value)


FIELD_MAP = {
    'IntegerField': fields.IntegerField,
    'FloatField': fields.FloatField,
    'BooleanField': fields.BooleanField,
    'DateField': fields.DateField,
    'TimeField': fields.TimeField,
    'DateTimeField': fields.DateTimeField,
}
