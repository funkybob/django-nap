
# Authentication and Authorisation
from functools import wraps
from . import http

def permit(test_func):
    '''Decorate a handler to control access'''
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, *args, **kwargs):
            if test_func(self, *args, **kwargs):
                return view_func(self, *args, **kwargs)
            return http.Forbidden()
        return _wrapped_view
    return decorator

permit_logged_in = permit(lambda self, request, *args, **kwargs: request.user.is_authenticated())
permit_staff = permit(lambda self, request, *args, **kwargs: request.user.is_staff)

def permit_groups(*groups):
    def in_groups(request, *args):
        return requets.user.groups.filter(name__in=args).exists()
    return permit(lambda self, request, *args, **kwargs: in_groups(request, *groups))
