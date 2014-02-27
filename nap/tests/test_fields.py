
from django.test import TestCase

from nap import fields
from nap.exceptions import ValidationError

class Mock(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class FieldTestCase(TestCase):
    '''
    Field cycles:
    deflate: digattr -> reduce -> data[name]
    inflate: data[name] -> restore -> dest[name]
    '''

    def test_000_field(self):
        data = {}
        field = fields.Field()

        field.deflate('value', Mock(value='str'), data)
        self.assertEqual('str', data['value'])

        dest = {}

        field.inflate('value', data, dest)
        self.assertEqual(dest['value'], data['value'])

    def test_000_field_none(self):
        '''None is treated specially.'''
        data = {}
        field = fields.Field()

        field.deflate('value', Mock(value=None), data)
        self.assertTrue(data['value'] is None)

        dest = {}

        field.inflate('value', data, dest)
        self.assertEqual(data['value'], dest['value'])

    def test_000_field_default(self):
        '''
        With no default set, we can't deflate a field with no value.
        '''
        data = {}
        field = fields.Field()

        with self.assertRaises(AttributeError):
            field.deflate('value', Mock(), data)

    def test_000_readonly(self):
        data = {'value': 1}
        dest = {}
        field = fields.Field(readonly=True)
        field.inflate('value', data, dest)
        self.assertNotIn('value', dest)

    def test_000_nodefault(self):
        data = {}
        dest = {}
        field = fields.Field()
        field.inflate('value', data, dest)
        self.assertNotIn('value', dest)

    def test_000_default(self):
        data = {}
        dest = {}
        field = fields.Field(default=1)

        field.inflate('value', data, dest)
        self.assertEqual(dest['value'], 1)

    def test_000_notnull(self):
        data = {'value': None}
        dest = {}
        field = fields.Field(null=False)

        with self.assertRaises(ValidationError):
            field.inflate('value', data, dest)

    def test_001_boolean(self):
        data = {}
        field = fields.BooleanField()

        field.deflate('value', Mock(value=True), data)
        self.assertTrue(data['value'] is True)

        dest = {}

        field.inflate('value', data, dest)
        self.assertTrue(dest['value'] is True)

    def test_002_integer(self):
        data = {}
        field = fields.IntegerField()

        field.deflate('value', Mock(value=7), data)
        self.assertEqual(data['value'], 7)

        dest = {}

        field.inflate('value', data, dest)
        self.assertEqual(dest['value'], data['value'])

    def test_003_decimal(self):
        from decimal import Decimal
        data = {}
        field = fields.DecimalField()

        field.deflate('value', Mock(value=Decimal('1.05')), data)
        # JS has no Decimal type, only float
        self.assertEqual(data['value'], 1.05)

        dest = {}

        field.inflate('value', data, dest)
        self.assertEqual(dest['value'], data['value'])

    def test_004_datetime(self):
        from datetime import datetime
        data = {}
        field = fields.DateTimeField()

        when = datetime(2010, 11, 5, 12, 7, 19)
        field.deflate('value', Mock(value=when), data)
        self.assertEqual(data['value'], '2010-11-05 12:07:19')

        dest = {}

        field.inflate('value', data, dest)
        self.assertEqual(dest['value'], when)

    def test_005_date(self):
        from datetime import date
        data = {}
        field = fields.DateField()

        when = date(2010, 11, 5)
        field.deflate('value', Mock(value=when), data)
        self.assertEqual(data['value'], '2010-11-05')

        dest = {}

        field.inflate('value', data, dest)
        self.assertEqual(dest['value'], when)

    def test_006_time(self):
        from datetime import time
        data = {}
        field = fields.TimeField()

        when = time(12, 7, 19)
        field.deflate('value', Mock(value=when), data)
        self.assertEqual(data['value'], '12:07:19')

        dest = {}

        field.inflate('value', data, dest)
        self.assertEqual(dest['value'], when)

    def test_007_serialiser(self):
        from nap.serialiser import Serialiser
        class SimpleSerialiser(Serialiser):
            a = fields.Field()
            b = fields.Field()
            c = fields.Field()

        data = {}
        field = fields.SerialiserField(serialiser=SimpleSerialiser())

        value = Mock(value=Mock(a=1, b='two', c=3.0))
        field.deflate('value', value, data)
        self.assertEqual(data['value']['a'], 1)
        self.assertEqual(data['value']['b'], 'two')
        self.assertEqual(data['value']['c'], 3.0)

