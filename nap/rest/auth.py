
from nap import auth


class AuthorisationMixin(object):
    '''
    Mixin class to help decorating the view function returned by ``as_view``.
    '''

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        view = super(LoginView, cls).as_view(*args, **kwargs)
        return self.permit(view)


class LoginRequiredMixin(object):

    @auth.permit_logged_in
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class StaffRequiredMixin(object):

    @auth.permit_staff
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
