
# Authentication and Authorisation
from functools import wraps

class NullAuthorise(object):

    def may(self, request, action, object_id=None, **kwargs):
        return True

class DjangoAuthorise(object):
    '''Permissions based on Django's'''
    def may(self, request, action, object_id=None, **kwargs):
        if not request.user.is_authenticated():
            return request.method == 'GET'

        # Logically these permissions only apply to basic CRUD
        opts = self.model._meta

        if action == 'default':
            if request.method == 'POST' and object_id is None:
                return request.user.has_perm('.'.join([
                    opts.app_label,
                    opts.get_add_permission()
                ]))
            elif request.method == 'PUT' and object_id:
                return request.user.has_perm('.'.join([
                    opts.app_label,
                    opts.get_change_permission()
                ]))
            elif request.method == 'DELETE' and object_id:
                return request.user.has_perm('.'.join([
                    opts.app_label,
                    opts.get_delete_permission()
                ]))
        return False


class BaseAuthorise(object):
    '''
    Helper class to make targeting specific endpoints easier.

    Follows the same pattern as finding a handler, but prefixes
    the method name with 'may_'
    '''
    may_default = True
    def may(self, request, action, object_id=None, **kwargs):
        prefix = 'list' if object_id is None else 'object'
        method = request.method.lower()
        handler = getattr(self, 'may_%s_%s_%s' % (
            prefix,
            method,
            action
        ), None)
        if handler is None:
            handler = getattr(self, 'may_%s_%s' % (
                prefix, action,
            ), None)
        if handler is None:
            return self.may_default
        return handler(request, action, object_id, **kwargs)
        
def permit(test_func):
    '''Decorate a handler to control access'''
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, *args, **kwargs):
            if test_func(self, *args, **kwargs):
                return view_func(*args, **kwargs)
            return http.HttpResponseUnauthorized()
        return _wrapped_view
    return decorator

permit_logged_in = permit(lambda self, request, *args, **kwargs: request.user.is_authenticated())
permit_staff = permit(lambda self, request, *args, **kwargs: request.user.is_staff)

