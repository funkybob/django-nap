
from .fields import Field
from .views import DataView

from django.utils.six import with_metaclass


class MetaView(type):

    def __new__(mcs, name, bases, attrs):
        meta = attrs.get('Meta', None)

        try:
            model = meta.model
        except AttributeError:
            if name != 'ModelDataView':
                raise
        else:
            include = getattr(meta, 'fields', None)
            exclude = getattr(meta, 'exclude', [])

            # XXX Does the top base have all fields?

            for model_field in model._meta.fields:
                if model_field.name in attrs:
                    continue
                if model_field.name in exclude:
                    continue
                if include != '__all__' and model_field.name not in include:
                    continue

                # XXX Magic for field types
                attrs[model_field.name] = Field(model_field.name)

        attrs['_meta'] = meta

        return super(MetaView, mcs).__new__(mcs, name, bases, attrs)


class ModelDataView(with_metaclass(MetaView, DataView)):

    pass
