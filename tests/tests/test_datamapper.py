
from django.test import TestCase
from django.core.exceptions import ValidationError

from nap import datamapper
from nap.datamapper.filters import NotNullFilter


class TestMapper(datamapper.DataMapper):
    @datamapper.field
    def readonly(self):
        return True

    value = datamapper.Field('value')
    required = datamapper.Field('required', required=True)


class TestObj(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class MapperTest(TestCase):

    def test_000_assurance(self):
        o = TestObj(readonly=False, value='foo')
        m = TestMapper(o)

        d = m._reduce()

        self.assertEqual(d['readonly'], True)
        self.assertEqual(d['value'], 'foo')

    def test_001_update(self):
        m = TestMapper()
        m._apply({'value': 1})

        self.assertEqual(m._obj['value'], 1)

    def test_002_readonly(self):
        m = TestMapper()
        with self.assertRaises(AttributeError):
            m._apply({'readonly', False})

    def test_003_validate(self):
        m = TestMapper()

        m._apply({})

        with self.assertRaises(ValidationError):
            m._apply({}, full=True)
