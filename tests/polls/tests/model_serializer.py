from django.test import TestCase
from polls import models
from nap.serialiser import ModelSerialiser
from nap.publisher import Publisher


class PollSerialiser(ModelSerialiser):
    class Meta:
        model = models.Poll


class PollPublisher(Publisher):
    serialiser = PollSerialiser()
    api_name = 'polls'

    def get_object_list(self):
        return models.Poll.objects.all()

from nap import api
api.register('v1', PollPublisher)


class ModelSerializerTest(TestCase):

    def test_model_fields(self):
        serializer = PollSerialiser()
        self.assertTrue(len(serializer._fields) == 3)
