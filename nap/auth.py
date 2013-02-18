
# Authentication and Authorisation
from functools import wraps

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

