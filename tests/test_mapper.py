
from django.test import TestCase
from django.core.exceptions import ValidationError

from nap.mapper import Mapper, field, Field


class TestMapper(Mapper):
    @field(readonly=True)
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
        class DM(Mapper):
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

    def test_005_inheritance(self):
        class Parent(Mapper):
            @field
            def f(self):
                return self.f

        class Child(Parent):
            @field
            def g(self):
                return self.g

        o = TestObj(f=1, g=2)
        p = Parent(o)
        c = Child(o)

        dp = p << o
        dc = c << o

        self.assertEqual(dp, {'f': 1})
        self.assertEqual(dc, {'f': 1, 'g': 2})

    def test_006_shortcuts(self):
        o = TestObj(value=0)
        m = TestMapper(o)

        oo = {'value': 1} >> m
        self.assertTrue(o is oo)
        self.assertEqual(o.value, 1)
