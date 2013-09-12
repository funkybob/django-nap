
from nap.models import ModelSerialiser
from nap.serialiser import Serialiser
from nap import fields

from .models import Choice

class ChoiceSerialiser(ModelSerialiser):
    class Meta:
        model = Choice
        exclude = ('poll,')

class PollSerialiser(Serialiser):
    question = fields.Field()
    published = fields.DateTimeField('pub_date')
    choices = fields.ManySerialiserField(serialiser=ChoiceSerialiser())

