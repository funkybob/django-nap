from django.core.exceptions import ValidationError
from django.views.generic.list import MultipleObjectMixin

from .base import MapperMixin, NapView


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
        '''
        Returns an ok_response
        '''
        return self.ok_response()


class ListPostMixin:

    def post(self, request, *args, **kwargs):
        '''
        Handle POST on a List view.

        Validates the data against the `model_class`, and calls `post_valid` or
        `post_invalid` as appropriate.
        '''
        self.mapper = self.get_mapper(self.model())
        self.data = self.get_request_data()

        try:
            self.object = self.mapper._apply(self.data)
        except ValidationError:
            return self.post_invalid(self.mapper._errors)

        return self.post_valid()

    def post_invalid(self, errors):
        '''
        Called on invalid POST data.

        Returns an `error_response`.
        '''
        return self.error_response(errors)

    def post_valid(self, **kwargs):
        '''
        Called on valid POST data.

        Saves self.object and returns a `created_response`.
        '''
        self.object.save()

        return self.created_response(**kwargs)


class ListBaseView(ListMixin, NapView):
    '''
    A Subclass of ListMixin and NapView.
    '''
    pass
