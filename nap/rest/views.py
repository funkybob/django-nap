from django.core.exceptions import ValidationError
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .. import http
from ..utils import JsonMixin, flatten_errors


class NapView(View):
    '''
    Base view for Nap CBV.

    Catches any http exceptions raised, and returns them.
    '''

    def dispatch(self, *args, **kwargs):
        '''
        If any code raises one of our HTTP responses, we should catch and
        return it.
        '''
        try:
            return super().dispatch(*args, **kwargs)
        except http.BaseHttpResponse as exc:
            return exc


class MapperMixin(JsonMixin):
    '''
    Base class for generating JSON responses using Mappers.
    '''
    response_class = http.JsonResponse
    content_type = 'application/json'
    mapper_class = None

    # Defaults for safety
    object = None
    object_list = None
    mapper = None

    ok_status = http.STATUS.OK
    accepted_status = http.STATUS.ACCEPTED
    created_status = http.STATUS.CREATED
    deleted_status = http.STATUS.NO_CONTENT
    error_status = http.STATUS.BAD_REQUEST

    def get_mapper(self, obj=None):
        '''
        Get the mapper to use for this request.

        Default action is to use self.mapper_class
        '''
        return self.mapper_class(obj)

    def empty_response(self, **kwargs):
        '''
        Helper method to return an empty response.
        '''
        kwargs.setdefault('safe', False)
        return self.response_class('', **kwargs)

    def single_response(self, **kwargs):
        '''
        Helper method to return a single object.

        If `object` is not passed, it will try to use `self.object`.  If
        `self.object` is not set, it will call `self.get_object()`.

        If `mapper` is not passed, it will try to use `self.mapper`.  If
        `self.mapper` is not set, it will call `self.get_mapper()`.

        Returns a `self.response_class` instance, passed ``mapper << obj``,
        along with `**kwargs`.
        '''
        obj = kwargs.pop('object', self.object)
        if obj is None:
            obj = self.get_object()

        mapper = kwargs.pop('mapper', self.mapper)
        if mapper is None:
            mapper = self.get_mapper(obj)

        return self.response_class(mapper << obj, **kwargs)

    def multiple_response(self, **kwargs):
        '''
        Helper method to return an iterable of objects.

        If `object_list` is not passed, it will try to use `self.obect_list`.
        If `self.object_list` is not set, it will call
        `self.get_object_list()`.

        If `mapper` is not passed, it will try to use `self.mapper`.  If
        `self.mapper` is not set, it will call `self.get_mapper()`.

        Returns a `self.response_class` instance, passed a list of ``mapper <<
        obj`` applied to each object, along with `**kwargs`.
        '''
        kwargs.setdefault('safe', False)

        object_list = kwargs.pop('object_list', self.object_list)
        if object_list is None:
            object_list = self.get_queryset()

        mapper = kwargs.pop('mapper', self.mapper)
        if mapper is None:
            mapper = self.get_mapper()

        page_size = self.get_paginate_by(object_list)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(object_list, page_size)
        else:
            paginator = page = None
            is_paginated = False

        data = [mapper << obj for obj in object_list]

        if page_size:
            if is_paginated:
                meta = {
                    'offset': page.start_index() - 1,
                    'page': page.number,
                    'total': paginator.count,
                }
            else:
                meta = {}
            return self.response_class({
                'meta': meta,
                'data': data,
            }, **kwargs)

        return self.response_class(data, **kwargs)

    def accepted_response(self, **kwargs):
        '''
        Shortcut to return an ``empty_response`` using a ``status`` of
        ``self.accepted_status``.
        '''
        kwargs.setdefault('status', self.accepted_status)
        return self.empty_response(**kwargs)

    def created_response(self, **kwargs):
        '''
        Shortcut to return a ``single_response`` using a ``status`` of
        ``self.created_status``.
        '''
        kwargs.setdefault('status', self.created_status)
        return self.single_response(**kwargs)

    def deleted_response(self, **kwargs):
        '''
        Shortcut to return an ``empty_response`` using a ``status`` of
        ``self.deleted_status``.
        '''
        kwargs.setdefault('status', self.deleted_status)
        return self.empty_response(**kwargs)

    def error_response(self, errors):
        '''
        Helper method to return ``self.respone_class`` with a ``status`` of
        ``self.error_status``.

        Will flatten ``errors`` using ``flatten_error``.
        '''
        return self.response_class(
            flatten_errors(errors),
            status=self.error_status,
        )


# List views
class ListMixin(MapperMixin, MultipleObjectMixin):

    def ok_response(self, **kwargs):
        '''
        Shortcut to return a ``multiple_response`` with a ``status`` of
        ``self.ok_status``.
        '''
        kwargs.setdefault('status', self.ok_status)
        return self.multiple_response(**kwargs)


class ListGetMixin:

    def get(self, request, *args, **kwargs):
        return self.ok_response()


class ListPostMixin:

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

    def post_valid(self, **kwargs):
        self.object.save()

        return self.created_response(**kwargs)


class BaseListView(ListMixin, NapView):
    pass


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
        except ValidationError as e:
            return self.put_invalid(e.error_dict)

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
        except ValidationError as e:
            return self.patch_invalid(e.error_dict)

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


class BaseObjectView(ObjectMixin, NapView):
    pass
