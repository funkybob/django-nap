from django.test import TestCase
from polls import models
from nap.models import ModelSerialiser
from nap.publisher import Publisher
from nap import api


class PollSerialiser(ModelSerialiser):
    class Meta:
        model = models.Poll


class PollPublisher(Publisher):
    serialiser = PollSerialiser()
    api_name = 'polls'

    def get_object_list(self):
        return models.Poll.objects.all()


class ApiTest(TestCase):

    def tearDown(self):
        try:
            del api.APIS['v1']
        except KeyError:
            pass

    def test_patterns(self):
        self.assertTrue(api.patterns() == [])

    def test_register(self):
        self.assertTrue(len(api.APIS.keys()) == 0)
        api.register('v1', PollPublisher)
        self.assertTrue(len(api.APIS.keys()) == 1)
        self.assertTrue(len(api.patterns()) == 1)
