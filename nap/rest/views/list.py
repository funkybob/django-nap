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
        return self.ok_response()


class ListPostMixin:

    def post(self, request, *args, **kwargs):
        self.mapper = self.get_mapper(self.model())
        self.data = self.get_request_data()

        try:
            self.object = self.mapper._apply(self.data)
        except ValidationError as e:
            return self.post_invalid(e.error_dict)

        return self.post_valid()

    def post_invalid(self, errors):
        return self.error_response(errors)

    def post_valid(self, **kwargs):
        self.object.save()

        return self.created_response(**kwargs)


class ListBaseView(ListMixin, NapView):
    pass
