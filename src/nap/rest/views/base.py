from django.views.generic import View

from nap import http
from nap.http.decorators import except_response
from nap.utils import JsonMixin


class NapView(View):
    '''
    Base view for Nap CBV.

    Catches any http exceptions raised, and returns them instead.
    '''

    @classmethod
    def as_view(cls, **initkwargs):
        '''
        If any code raises one of our HTTP responses, we should catch and
        return it.
        '''
        return except_response(super().as_view(**initkwargs))


class MapperMixin(JsonMixin):
    '''
    Base class for generating JSON responses using Mappers.
    '''
    response_class = http.JsonResponse
    content_type = 'application/json'
    mapper_class = None
    include_meta = False

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
        try:
            obj = kwargs.pop('object')
        except KeyError:
            try:
                obj = self.object
            except AttributeError:
                obj = self.get_object()

        try:
            mapper = kwargs.pop('mapper')
        except KeyError:
            try:
                mapper = self.mapper
            except AttributeError:
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

        try:
            object_list = kwargs.pop('object_list')
        except KeyError:
            try:
                object_list = self.object_list
            except AttributeError:
                object_list = self.get_queryset()

        try:
            mapper = kwargs.pop('mapper')
        except KeyError:
            try:
                mapper = self.mapper
            except AttributeError:
                mapper = self.get_mapper()

        page_size = self.get_paginate_by(object_list)
        if page_size:
            paginator, page, object_list, is_paginated = self.paginate_queryset(object_list, page_size)
        else:
            paginator = page = None
            is_paginated = False

        data = [mapper << obj for obj in object_list]

        if page_size or self.include_meta:
            meta = self.get_meta(page)
            data = {
                'meta': meta,
                'data': data,
            }

        return self.response_class(data, **kwargs)

    def get_meta(self, page):
        if not page:
            return {}
        return {
            'offset': page.start_index() - 1,
            'page': page.number,
            'total': page.paginator.count,
        }

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

        Will flatten ``errors`` using ``get_json_data``.
        '''
        return self.response_class(
            errors.get_json_data(),
            status=self.error_status,
        )
