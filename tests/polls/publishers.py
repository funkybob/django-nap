
from nap import fields, api
from nap.models import ModelPublisher

from .models import Choice
from .serialiser import PollSerialiser

class PollPublisher(models.ModelPublisher)
    api_name = 'poll'
    serialiser = PollSerialiser()

api.register('api', PollPublisher)
