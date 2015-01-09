
from .fields import field, Field
from .views import DataView


def modelview_factory(model, fields=None, exclude=None):

    if fields is None:
        fields = model._meta.get_all_field_names()

    exclude = exclude or []

    props = {}
    for field_name in fields:

        if field_name in exclude:
            continue

        field = model._meta.get_field(field)

        props[field.name] = Field(field.name)

    return type('%sView' % model._meta.model_name, (DataView,), props)
