from types import SimpleNamespace

from django.test import TestCase


from nap.mapper import Mapper, fields


class FieldTestCase(TestCase):

    def test_field(self):
        class TestMapper(Mapper):
            foo = fields.Field('bar')

        o = SimpleNamespace(bar=1)
        m = TestMapper(o)

        self.assertEqual(m.foo, 1)

        m.foo = 2
        self.assertEqual(o.bar, 2)

    def test_readonly(self):
        class TestMapper(Mapper):
            foo = fields.Field('bar', readonly=True)

        o = SimpleNamespace(bar=1)
        m = TestMapper(o)

        with self.assertRaises(AttributeError):
            m.foo = 2
            self.assertEqual(o.bar, 1)

        m._apply({'foo': 2})
        self.assertEqual(o.bar, 1)

    def test_boolean_field(self):
        class TestMapper(Mapper):
            foo = fields.BooleanField('bar')

        o = SimpleNamespace(bar=True)
        m = TestMapper(o)

        d = m._reduce()
        self.assertEqual(d, {'foo': True})

        m._apply({'foo': False})
        self.assertEqual(o.bar, False)

        m.foo = 'Y'
        self.assertTrue(o.bar)

    def test_integer_field(self):
        class TestMapper(Mapper):
            foo = fields.IntegerField('bar')

        o = SimpleNamespace(bar=1)
        m = TestMapper(o)

        self.assertEqual(m.foo, 1)

        m.foo = '7'
        self.assertEqual(o.bar, 7)

    def test_float_field(self):
        class TestMapper(Mapper):
            foo = fields.FloatField('bar')

        o = SimpleNamespace(bar=1.0)
        m = TestMapper(o)

        self.assertEqual(m.foo, 1.0)

        m.foo = '7'
        self.assertEqual(o.bar, 7.0)
