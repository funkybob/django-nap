'''
Mixins for using Mappers with Publisher
'''
from django.core.exceptions import ValidationError

from nap import http
from nap.utils import flatten_errors


class MapperListMixin(object):

    def list_get_default(self, request, action, object_id):
        '''
        Replace the default list handler with one that returns a flat list.
        '''
        object_list = self.get_object_list()
        object_list = self.filter_object_list(object_list)
        object_list = self.sort_object_list(object_list)

        mapper = self.mapper()

        data = [
            mapper << obj
            for obj in object_list
        ]
        return self.create_response(data)


class MapperDetailMixin(object):

    def object_get_default(self, request, action, object_id):
        obj = self.get_object(object_id)

        mapper = self.mapper(obj)

        return self.create_response(mapper._reduce())


class MapperPostMixin(object):
    '''
    Generic handling of POST-to-create
    '''
    def list_post_default(self, request, action, object_id):
        data = self.get_request_data({})

        mapper = self.mapper(self.model())
        try:
            obj = mapper._apply(data, full=True)
        except ValidationError as e:
            return self.post_invalid(e.error_dict)
        else:
            return self.post_valid(obj)

    def post_valid(self, obj):
        obj.save()
        return http.Created()

    def post_invalid(self, errors):
        return self.create_response(flatten_errors(errors),
            response_class=http.BadRequest)


class PutMixin(object):
    '''
    Generic handling of PUT-to-update
    '''
    def object_put_default(self, request, action, object_id):
        data = self.get_request_data({})

        obj = self.get_object(object_id)

        mapper = self.mapper(obj)
        try:
            mapper._apply(data)
        except ValidationError as e:
            return self.put_invalid(obj, e.error_dict)

        return self.put_valid(obj, data)

        return http.Accepted()

    def put_valid(self, obj, data):
        '''
        Hook to control updating of objects.

        Will be passes the unsaved updated model instance.
        Default: save the object.
        '''
        obj.save()
        return obj

    def put_invalid(self, obj, errors):
        return self.create_response(flatten_errors(errors),
            response_class=http.BadRequest)


class DeleteMixin(object):
    '''
    Generic handling of DELETE-to-disable
    '''
    def object_delete_default(self, request, action, object_id):
        obj = self.get_object(object_id)

        self.delete_object(obj)
        return http.ResetContent()

    def delete_object(self, obj):
        '''
        Hook to allow control of how to delete an instance.
        '''
        obj.delete()
