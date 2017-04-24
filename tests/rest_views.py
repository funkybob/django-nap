from nap.datamapper.models import ModelDataMapper
from nap.rest import views

from .models import Poll


class PollMapper(ModelDataMapper):
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
