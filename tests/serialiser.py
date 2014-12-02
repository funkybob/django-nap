
from nap import serialiser

from .models import Choice

class ChoiceSerialiser(serialiser.ModelSerialiser):
    class Meta:
        model = Choice
        exclude = ('poll,')

    votes = serialiser.Field('vote_count')

class PollSerialiser(serialiser.Serialiser):
    question = serialiser.Field()
    published = serialiser.DateTimeField('pub_date')
    choices = serialiser.ManySerialiserField(serialiser=ChoiceSerialiser())
