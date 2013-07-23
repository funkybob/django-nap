
from nap import models, fields, api, serialiser, publisher

from .models import Choice, Poll


class ChoiceSerialiser(models.ModelSerialiser):

    class Meta:
        model = Choice
        exclude = ('poll,')


class PollSerialiser(serialiser.Serialiser):
    api_name = 'poll'

    question = fields.Field()
    published = fields.DateTimeField('pub_date')
    choices = fields.ManySerialiserField('choices_set.all', serialiser=ChoiceSerialiser())


class PollPublisher(publisher.Publisher):
    serialiser = PollSerialiser()
    api_name = 'polls'

    def get_object_list(self):
        return Poll.objects.all()


api.register('api', PollPublisher)
