from __future__ import unicode_literals

from . import fields, http
from .serialiser import MetaSerialiser, Serialiser
from .publisher import Publisher

from six import with_metaclass

from django.db.models import Manager
from django.db.models.fields import NOT_PROVIDED
from django.shortcuts import get_object_or_404

FIELD_MAP = {}
# Auto-construct the field map
for f in dir(fields):
    cls = getattr(fields, f)
    try:
        if issubclass(cls, fields.Field):
            FIELD_MAP[f] = cls
    except TypeError:
        pass

class MetaModelSerialiser(MetaSerialiser):
    def __new__(mcs, name, bases, attrs):

        new_class = super(MetaModelSerialiser, mcs).__new__(mcs, name, bases, attrs)

        include = getattr(new_class._meta, 'fields', [])
        exclude = getattr(new_class._meta, 'exclude', [])
        read_only = getattr(new_class._meta, 'read_only_fields', [])

        current_fields = new_class._fields.keys()

        model_fields = {}
        try:
            model = new_class._meta.model
        except AttributeError:
            pass
        else:
            for field in model._meta.fields:
                # If we've got one, skip...
                if field.name in current_fields:
                    continue

                # If we have a whitelist, and it's not in it, skip
                if include and not field.name in include:
                    continue

                # If it's blacklisted, skip
                if field.name in exclude:
                    continue

                kwargs = {
                    'readonly': field.name in read_only,
                    'null': field.null,
                }
                if not field.default is NOT_PROVIDED:
                    kwargs['default'] = field.default

                field_class = FIELD_MAP.get(field.__class__.__name__, fields.Field)
                model_fields[field.name ] = field_class(**kwargs)

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


class ModelPublisher(Publisher):
    '''A Publisher with useful methods to publish Models'''

    @property
    def model(self):
        '''By default, we try to get the model from our serialiser'''
        # XXX Should this call get_serialiser?
        return self.serialiser._meta.model

    # Auto-build serialiser from model class?

    def get_object_list(self):
        return self.model.objects.all()

    def get_object(self, object_id):
        return get_object_or_404(self.get_object_list(), pk=object_id)



class ModelFormMixin(object):
    '''Provide writable models using form validation'''

    initial = {}
    form_class = None

    # Here we mimic the FormMixin from django
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.initial.copy()

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.form_class

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self, **kwargs):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs.setdefault('initial', self.get_initial())
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def list_post_default(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            obj = form.save()
            return self.render_single_object(obj)

        # return errors


    def object_put_default(self, request, object_id, *args, **kwargs):
        obj = self.get_object(object_id)
        form_class = self.get_form_class()
        form = self.get_form(form_class, instance=obj)

        if form.is_valid():
            obj = form.save()
            return self.render_single_object(obj)

        # return errors

    def object_delete_default(self, request, object_id, *args, **kwargs):
        obj = self.get_object(object_id)
        # XXX Some sort of verification?
        obj.delete()
        return http.NoContent()


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
        if not 'serialiser' in kwargs:
            model = kwargs.pop('model')
            kwargs['serialiser'] = modelserialiser_factory(model.__name__ + 'Serialiser', model, **kwargs)()
        super(ModelSerialiserField, self).__init__(*args, **kwargs)

class ModelManySerialiserField(fields.ManySerialiserField):
    def __init__(self, *args, **kwargs):
        if not 'serialiser' in kwargs:
            model = kwargs.pop('model')
            kwargs['serialiser'] = modelserialiser_factory(model.__name__ + 'Serialiser', model, **kwargs)()
        super(ModelManySerialiserField, self).__init__(*args, **kwargs)

    def reduce(self, value, **kwargs):
        if isinstance(value, Manager):
            value = value.all()
        return super(ModelManySerialiserField, self).reduce(value, **kwargs)
