
from . import fields
from .meta import Meta
from .serialiser import MetaSerialiser, Serialiser
from .publisher import Publisher

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
                    'readonly': f.name in read_only,
                }

                field_class = FIELD_MAP.get(f.__class__.__name__, fields.Field)
                new_class._fields[f.name] = field_class(**kwargs)
        except AttributeError:
            pass

        return new_class


class ModelSerialiser(Serialiser):
    __metaclass__ = MetaModelSerialiser

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
    try:
        attrs['fields'] = kwargs['fields']
    except KeyError:
        pass
    try:
        attrs['exclude'] = kwargs['exclude']
    except KeyError:
        pass

    meta = type('Meta', (object,), attrs)
    return type(ModelSerialiser)(name, (ModelSerialiser,), {'Meta': meta})

class ModelSerialiserField(fields.SerialiserField):
    def __init__(self, serialiser=None, model=None, *args, **kwargs):
        if serialiser is None:
            serialiser = modelserialiser_factory(model.__name__ + 'Serialiser', model, **kwargs)()
        super(ModelSerialiserField, self).__init__(serialiser, *args, **kwargs)

class ModelManySerialiserField(fields.ManySerialiserField):
    def __init__(self, serialiser=None, model=None, *args, **kwargs):
        if serialiser is None:
            serialiser = modelserialiser_factory(model.__name__ + 'Serialiser', model, **kwargs)()
        super(ModelManySerialiserField, self).__init__(serialiser, *args, **kwargs)

