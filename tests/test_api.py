from django.test import TestCase
from nap.serialiser import ModelSerialiser
from nap import rest

from . import models


class PollSerialiser(ModelSerialiser):
    class Meta:
        model = models.Poll


class PollPublisher(rest.Publisher):
    serialiser = PollSerialiser()
    api_name = 'polls'

    def get_object_list(self):
        return models.Poll.objects.all()


class ApiTest(TestCase):

    def tearDown(self):
        try:
            del rest.api.APIS['v1']
        except KeyError:
            pass

    def test_patterns(self):
        self.assertTrue(rest.api.patterns() == [])

    def test_register(self):
        self.assertTrue(len(rest.api.APIS.keys()) == 0)
        rest.api.register('v1', PollPublisher)
        self.assertTrue(len(rest.api.APIS.keys()) == 1)
        self.assertTrue(len(rest.api.patterns()) == 1)
