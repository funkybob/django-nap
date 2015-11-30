from __future__ import unicode_literals

# Authentication and Authorisation
from functools import wraps

from . import http


def permit(test_func, response_class=http.Forbidden):
    '''Decorate a handler to control access'''
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, *args, **kwargs):
            if test_func(self, *args, **kwargs):
                return view_func(self, *args, **kwargs)
            return response_class()
        return _wrapped_view
    return decorator


# Helpers for people wanting to control response class
def test_logged_in(self, *args, **kwargs):
    return self.request.user.is_authenticated()


def test_staff(self, *args, **kwargs):
    return self.request.user.is_staff

permit_logged_in = permit(test_logged_in)
permit_staff = permit(test_staff)


def permit_groups(response_class=http.Forbidden, *groups):
    def in_groups(self, *args, **kwargs):
        return self.request.user.groups.filter(name__in=groups).exists()
    return permit(in_groups, response_class=response_class)
