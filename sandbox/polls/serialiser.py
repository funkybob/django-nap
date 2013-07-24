
from nap import models, fields, api, serialiser, publisher

from .models import Choice, Poll


class ChoiceSerialiser(models.ModelSerialiser):
    poll = models.ModelSerialiserField(model=Poll, exclude=('choices',))

    class Meta:
        model = Choice

class ChoicePublisher(models.ModelPublisher):
    serialiser = ChoiceSerialiser()
    api_name = 'choice'


class PollSerialiser(serialiser.Serialiser):
    api_name = 'poll'

    question = fields.Field()
    published = fields.DateTimeField('pub_date')
    choices = models.ModelManySerialiserField('choice_set.all', model=Choice, exclude=('poll',))


class PollPublisher(publisher.Publisher):
    serialiser = PollSerialiser()
    api_name = 'polls'

    def get_object_list(self):
        return Poll.objects.all()


api.register('api', PollPublisher)
api.register('api', ChoicePublisher)
