
from .meta import Meta
from .models import ModelSerialiser


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

