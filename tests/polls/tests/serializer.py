from django.test import TestCase
from polls import models
from nap.serialiser import Serialiser
from nap.models import ModelSerialiser
from nap.fields import Field


class SerializerTest(TestCase):

    def test_declared_fields(self):
        class MySerialiser(Serialiser):
            test_field = Field()
            another_field = Field()

        serializer = MySerialiser()
        for f in ('test_field', 'another_field'):
            self.assertIn(f, serializer._fields.keys())


class ModelSerializerTest(TestCase):

    def test_model_fields(self):
        class PollSerialiser(ModelSerialiser):
            class Meta:
                model = models.Poll

        serializer = PollSerialiser()
        for f in ('id', 'question', 'pub_date'):
            self.assertIn(f, serializer._fields.keys())

    def test_model_fields_include(self):

        class PollSerialiser(ModelSerialiser):
            class Meta:
                model = models.Poll
                fields = ('question', 'pub_date')

        serializer = PollSerialiser()
        for f in ('question', 'pub_date'):
            self.assertIn(f, serializer._fields.keys())
        self.assertNotIn('id', serializer._fields.keys())

    def test_model_fields_exclude(self):

        class PollSerialiser(ModelSerialiser):
            class Meta:
                model = models.Poll
                exclude = ('id')

        serializer = PollSerialiser()
        for f in ('question', 'pub_date'):
            self.assertIn(f, serializer._fields.keys())
        self.assertNotIn('id', serializer._fields.keys())
