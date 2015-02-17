from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .. import http
from ..utils import JsonMixin, flatten_errors


class SerialisedResponseMixin(object):
    '''
    Passes context data through a
    '''
    content_type = 'application/json'
    response_class = http.JsonResponse

    def render_to_response(self, context, **response_kwargs):
        response_class = response_kwargs.pop('response_class', self.response_class)
        response_kwargs.setdefault('content_type', self.content_type)
        return response_class(context, **response_kwargs)


class MapperMixin(JsonMixin):
    response_class = http.JsonResponse
    content_type = 'application/json'
    mapper_class = None

    accepted_status = http.STATUS.ACCEPTED
    created_status = http.STATUS.CREATED
    deleted_status = http.STATUS.OK
    error_status = http.STATUS.BAD_REQUEST

    def get_mapper(self, obj=None):
        return self.mapper_class(obj)

    def accepted_response(self):
        return self.response_class('', status=self.accepted_status)

    def created_response(self):
        return self.response_class(
            self.mapper << self.object,
            status=self.created_status,
        )

    def deleted_response(self):
        return self.response_class(
            self.mapper << self.object,
            status=self.deleted_status,
        )

    def error_response(self, errors):
        return self.response_class(
            flatten_errors(errors),
            status=self.error_status,
        )


# List views
class ListMixin(MapperMixin, MultipleObjectMixin):
    pass


class ListGetMixin(object):

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        self.mapper = self.get_mapper()

        return self.response_class([
            self.mapper << obj
            for obj in self.object_list.all()
        ], safe=False)


class ListPostMixin(object):

    def post(self, request, *args, **kwargs):
        self.mapper = self.get_mapper(self.model())
        self.data = self.get_request_data()

        try:
            self.object = self.mapper._apply(self.data)
        except ValidationError as e:
            return self.post_invalid(e.error_dict)

        return self.post_valid()

    def post_invalid(self, errors):
        return self.error_response(errors)

    def post_valid(self):
        self.object.save()

        return self.created_response()


class ObjectMixin(MapperMixin, SingleObjectMixin):
    pass


class ObjectGetMixin(object):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.mapper = self.get_mapper(self.object)

        return self.response_class(self.mapper._reduce())


class ObjectPutMixin(object):

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.mapper = self.get_mapper(self.object)

        self.data = self.get_request_data({})

        try:
            self.mapper._patch(self.data)
        except ValidationError as e:
            return self.put_invalid(e.error_dict)

        return self.put_valid()

    def put_valid(self):
        self.object.save()
        return self.response_class(self.mapper._reduce())

    def put_invalid(self, errors):
        return self.error_response(errors)


class ObjectDeleteMixin(object):

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.mapper = self.get_mapper(self.object)

        return self.delete_valid()

    def delete_valid(self):
        self.object.delete()

        return self.deleted_response()
