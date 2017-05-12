from nap.mapper import ModelMapper
from nap.rest import views

from .models import Poll


class PollMapper(ModelMapper):
    class Meta:
        model = Poll
        fields = ['question', 'pub_date']


class PollMixin(object):
    model = Poll
    mapper_class = PollMapper


class PollListView(PollMixin,
                   views.ListGetMixin,
                   views.ListPostMixin,
                   views.BaseListView):
    pass


class SinglePollView(PollMixin,
                     views.ObjectGetMixin,
                     views.ObjectPutMixin,
                     views.ObjectPatchMixin,
                     views.ObjectDeleteMixin,
                     views.BaseObjectView):
    pass
