
from nap import rest
from nap.rest import api

from .serialiser import PollSerialiser


@api.register('api')
class PollPublisher(rest.ModelPublisher):
    api_name = 'poll'
    serialiser = PollSerialiser()
