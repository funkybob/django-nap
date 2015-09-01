
from django.test import TestCase
from django.core.exceptions import ValidationError

from nap.datamapper import DataMapper, field, Field
from nap.datamapper.filters import NotNullFilter, BooleanFilter, IntegerFilter


class TestMapper(DataMapper):
    @field
    def readonly(self):
        return True

    value = Field('value')
    required = Field('required', required=True)


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
        m._patch({'value': 1})

        self.assertEqual(m._obj['value'], 1)

    def test_002_readonly(self):
        m = TestMapper()
        with self.assertRaises(ValidationError):
            m._apply({'readonly': False})

    def test_003_validate(self):
        m = TestMapper()

        m._patch({})

        with self.assertRaises(ValidationError):
            m._apply({})

    def test_004_validation_error_params(self):
        class DM(DataMapper):
            @field
            def f(self):
                return None

            @f.setter
            def f(self, value):
                raise ValidationError("foo %(msg)s buz", params={'msg': "bar"})

        m = DM()
        with self.assertRaises(ValidationError) as cm:
            m._apply({'f': 'lorem'})
        self.assertEqual(cm.exception.messages, ["foo bar buz"])

        with self.assertRaises(ValidationError) as cm:
            m._patch({'f': 'lorem'})
        self.assertEqual(cm.exception.messages, ["foo bar buz"])


class FilterTest(TestCase):

    def test_000_not_null(self):
        class DM(DataMapper):
            f = Field('f', filters=[NotNullFilter])
            g = Field('g', filters=[NotNullFilter])

        m = DM()

        with self.assertRaises(ValidationError):
            m._apply({'f': None, 'g': 1})

    def test_001_boolean(self):
        class DM(DataMapper):
            f = Field('f', filters=[BooleanFilter])
            g = Field('g', filters=[BooleanFilter])
            h = Field('h', filters=[BooleanFilter])

        m = DM()

        m._apply({
            'f': 'False',
            'g': True,
            'h': None,
        })

        self.assertFalse(m._obj.f)
        self.assertTrue(m._obj.g)
        self.assertTrue(m._obj.h is None)

    def test_002_integer(self):
        class DM(DataMapper):
            f = Field('f', filters=[IntegerFilter])
            g = Field('g', filters=[IntegerFilter])
            h = Field('h', filters=[IntegerFilter])

        m = DM()

        m._apply({
            'f': 1,
            'g': '1',
            'h': None,
        })

        self.assertEqual(m._obj.f, 1)
        self.assertEqual(m._obj.g, 1)
        self.assertTrue(m._obj.h is None)

        with self.assertRaises(ValidationError):
            m._apply({'f': 'test'})
