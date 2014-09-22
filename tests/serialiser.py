
from nap import rest
from nap.rest import fields

from .models import Choice

class ChoiceSerialiser(rest.ModelSerialiser):
    class Meta:
        model = Choice
        exclude = ('poll,')


class PollSerialiser(rest.Serialiser):
    question = fields.Field()
    published = fields.DateTimeField('pub_date')
    choices = fields.ManySerialiserField(serialiser=ChoiceSerialiser())

