
from django.test import TestCase

from nap import fields

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
        data = {}
        field = fields.Field()

        field.deflate('value', Mock(), data)
        self.assertNotIn('value', data)

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

