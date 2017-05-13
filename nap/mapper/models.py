import datetime

from django.core.exceptions import ValidationError
from django.db.models.fields import NOT_PROVIDED

from .base import Mapper, MetaMapper as BaseMetaMapper
from .fields import field


class Options:
    def __init__(self, meta):
        self.model = getattr(meta, 'model', None)
        fields = getattr(meta, 'fields', [])
        if fields != '__all__':
            fields = list(fields)
        self.fields = fields
        self.exclude = list(getattr(meta, 'exclude', []))
        self.required = getattr(meta, 'required', {})
        self.readonly = getattr(meta, 'readonly', [])


class MetaMapper(BaseMetaMapper):

    def __new__(mcs, name, bases, attrs):
        meta = Options(attrs.get('Meta', None))

        if meta.model is None:
            if name != 'ModelMapper':
                raise ValueError('No model defined on class Meta.')
        else:
            existing = dict(bases[0]._fields)

            for f in meta.model._meta.get_fields():
                # Don't auto-add fields defined on this class
                if f.name in attrs:
                    continue
                if f.name in meta.exclude:
                    continue
                if meta.fields != '__all__' and \
                   f.name not in meta.fields:
                    # Ensure model validation is told to exclude this
                    meta.exclude.append(f.name)
                    continue

                # XXX Magic for field types
                kwargs = {
                    'readonly': f.name in meta.readonly or not f.editable,
                    'default': None if f.null and f.default is NOT_PROVIDED else f.default,
                    'required': meta.required.get(f.name, not f.blank),
                }

                field_class = _Field
                if f.is_relation:
                    kwargs['model'] = f.related_model
                    # OneToOneField or ForeignKey
                    if f.one_to_one or f.many_to_one:
                        field_class = ToOneField
                    # M2M on this model
                    elif f.many_to_many and not f.auto_created:
                        field_class = ToManyField
                else:
                    field_class = FIELD_MAP.get(f.__class__.__name__, _Field)

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


class _Field(field):
    def __init__(self, attr, *args, **kwargs):
        self.attr = attr
        # self.required = kwargs.pop('required', False)
        # self.default = kwargs.pop('default', NOT_PROVIDED)
        # self.readonly = kwargs.pop('readonly', False)
        super().__init__(*args, **kwargs)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        value = getattr(instance._obj, self.attr, self.default)
        if value is NOT_PROVIDED:
            raise AttributeError("'{}' has no attribute '{}'".format(
                cls.__name__,
                self.attr,
            ))
        return self.get(value)

    def __set__(self, instance, value):
        if self.readonly:
            raise AttributeError('Field {.name} is read-only.'.format(self))
        value = self.set(value)
        setattr(instance._obj, self.attr, value)

    def get(self, value):
        return value

    def set(self, value):
        return value


class BooleanField(_Field):
    def set(self, value):
        if value is None:
            return value
        if isinstance(value, bool):
            return value
        return value.lower() in (1, '1', 't', 'y', 'true')


class IntegerField(_Field):
    def get(self, value):
        return int(value)

    def set(self, value):
        return int(value)


class FloatField(_Field):
    def get(self, value):
        return float(value)

    def set(self, value):
        return float(value)


class TimeField(_Field):
    def get(self, value):
        if value is None:
            return value
        return value.replace(microsecond=0).isoformat()

    def set(self, value):
        if value is None or isinstance(value, datetime.time):
            return value
            return datetime.datetime.strptime(value, '%H:%M:%S').time()


class DateField(_Field):
    def get(self, value):
        if value is None:
            return value
        return value.isoformat()

    def set(self, value):
        if value is None or isinstance(value, datetime.date):
            return value
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()


class DateTimeField(_Field):
    def get(self, value):
        if value is None:
            return value
        return value.replace(microsecond=0).isoformat(' ')

    def set(self, value):
        if value is None or isinstance(value, datetime.datetime):
            return value
        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


class RelatedField(field):
    mapper = None

    def __init__(self, *args, model=None, mapper=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.related_model = model
        self.mapper = mapper


class ToOneField(RelatedField):

    def get(self, value):
        if self.mapper:
            return self.mapper(value)._reduce()
        return value.pk

    def set(self, value):
        if self.mapper:
            return self.mapper() << value
        return self.model.objects.get(pk=value)


class ToManyField(RelatedField):
    pass


FIELD_MAP = {
    'IntegerField': IntegerField,
    'FloatField': FloatField,
    'BooleanField': BooleanField,
    'DateField': DateField,
    'TimeField': TimeField,
    'DateTimeField': DateTimeField,
}
