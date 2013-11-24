
from django.test import TestCase
from django.test.client import RequestFactory

from nap import publisher

class TestPublisher(publisher.Publisher):
    pass


class PublisherTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.pub = TestPublisher(self.request)

    def test_000_index(self):
        data = self.pub.index()

        self.assertTrue('list' in data)
        self.assertTrue('object' in data)
