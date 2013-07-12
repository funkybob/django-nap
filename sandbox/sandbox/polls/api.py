from polls import models
from nap.models import ModelSerialiser
from nap.publisher import Publisher


class PollSerialiser(ModelSerialiser):
    class Meta:
        model = models.Poll


class PollPublisher(Publisher):
    serialiser = PollSerialiser()
    api_name = 'polls'

    def get_object_list(self):
        return models.Poll.objects.all()
