from django.core.exceptions import ValidationError
from django.views.generic.detail import SingleObjectMixin

from .base import MapperMixin, NapView


# Object views
class ObjectMixin(MapperMixin, SingleObjectMixin):

    def ok_response(self, **kwargs):
        kwargs.setdefault('status', self.ok_status)
        return self.single_response(**kwargs)


class ObjectGetMixin:

    def get(self, request, *args, **kwargs):
        return self.ok_response()


class ObjectPutMixin:

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.mapper = self.get_mapper(self.object)

        self.data = self.get_request_data({})

        try:
            self.mapper._apply(self.data)
        except ValidationError:
            return self.put_invalid(self.mapper._errors)

        return self.put_valid()

    def put_valid(self, **kwargs):
        self.object.save()
        return self.ok_response(**kwargs)

    def put_invalid(self, errors):
        return self.error_response(errors)


class ObjectPatchMixin:

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.mapper = self.get_mapper(self.object)

        self.data = self.get_request_data({})

        try:
            self.mapper._patch(self.data)
        except ValidationError:
            return self.patch_invalid(self.mapper._errors)

        return self.patch_valid()

    def patch_valid(self, **kwargs):
        self.object.save()
        return self.ok_response(**kwargs)

    def patch_invalid(self, errors):
        return self.error_response(errors)


class ObjectDeleteMixin:

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.mapper = self.get_mapper(self.object)

        return self.delete_valid()

    def delete_valid(self, **kwargs):
        self.object.delete()

        return self.deleted_response(**kwargs)


class ObjectBaseView(ObjectMixin, NapView):
    pass
