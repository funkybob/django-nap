from django.views.generic import View

from nap.datamapper.models import ModelDataMapper
from nap.rest import views

from .models import Poll


class PollMapper(ModelDataMapper):
    class Meta:
        model = Poll
        fields = ['question', 'pub_date']


class SinglePollView(views.ObjectGetMixin, views.ObjectPutMixin, views.ObjectPatchMixin, views.ObjectDeleteMixin, views.BaseObjectView):
    model = Poll
    mapper_class = PollMapper
