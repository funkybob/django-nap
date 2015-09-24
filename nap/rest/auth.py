
from nap import auth


class LoginRequiredMixin(object):

    @auth.permit_logged_in
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class StaffRequiredMixin(object):

    @auth.permit_staff
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
