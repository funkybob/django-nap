
from nap import serialiser
from nap.serialiser import fields

from .models import Choice

class ChoiceSerialiser(serialiser.ModelSerialiser):
    class Meta:
        model = Choice
        exclude = ('poll,')


class PollSerialiser(serialiser.Serialiser):
    question = fields.Field()
    published = fields.DateTimeField('pub_date')
    choices = fields.ManySerialiserField(serialiser=ChoiceSerialiser())

