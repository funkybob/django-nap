
from django.test import TestCase

from nap import serialiser


class TestSerialiser(serialiser.Serialiser):
    v_field = serialiser.Field('value')
    i_field = serialiser.IntegerField(null=True)
    c_field = serialiser.Field('complex')

    def deflate_c_field(self, obj, data, **kwargs):
        return True


class SerialiserTest(TestCase):

    def test_000_simple(self):
        ser = TestSerialiser()

        data = ser.object_deflate({
            'value': 'v',
            'i_field': 1,
            'complex': None,
        })

        self.assertEqual(data['v_field'], 'v')
        self.assertEqual(data['i_field'], 1)
        self.assertEqual(data['c_field'], True)
