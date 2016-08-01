from django.utils.decorators import classonlymethod

from nap import http


class AuthorisationMixin(object):
    '''
    Mixin class to help decorating the view function returned by ``as_view``.
    '''
    auth_response_class = http.Forbidden

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        view = super(LoginView, cls).as_view(*args, **kwargs)
        return self.permit(view)

    @classonlymethod
    def permit(cls, view):
        @wraps(view)
        def decorator(request, *args, **kwargs):
            if self.auth_test(request, *args, **kwargs):
                return view(request, *args, **kwargs)
            return self.auth_response_class()
        return decorator

    @classonlymethod
    def auth_test(cls, request, *args, **kwargs):
        return True


class LoginRequiredMixin(object):

    def auth_test(cls, request, *args, **kwargs):
        return request.user.is_authenticated()


class StaffRequiredMixin(object):

    def auth_test(cls, request, *args, **kwargs):
        return request.user.is_staff
