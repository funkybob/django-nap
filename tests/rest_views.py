from nap.mapper import ModelMapper
from nap.rest import views
from nap.shortcuts import get_object_or_404

from .models import Poll, Choice


class PollMapper(ModelMapper):
    class Meta:
        model = Poll
        fields = ['question', 'pub_date', 'kill_date']


class ChoiceMapper(ModelMapper):
    class Meta:
        model = Choice
        fields = '__all__'
        readonly = ('votes',)


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


class ChoiceMixin:
    model = Choice
    mapper_class = ChoiceMapper


class ChoiceListView(ChoiceMixin,
                     views.ListGetMixin,
                     views.ListPostMixin,
                     views.BaseListView):

    paginate_by = 1

    def get_queryset(self):
        return super().get_queryset().filter(poll__id=self.kwargs['poll_id'])

    def post_valid(self):
        self.object.poll = get_object_or_404(Poll, pk=self.kwargs['poll_id'])
        return super().post_valid()
