import datetime
from types import SimpleNamespace

from django.test import TestCase


from nap.mapper import Mapper, fields


class FieldTestCase(TestCase):

    def test_field_decorator(self):
        class TestMapper(Mapper):
            @fields.field
            def foo(self):
                return self.bar

        o = SimpleNamespace(bar=1)
        m = TestMapper(o)

        self.assertEqual(m.foo, 1)

        with self.assertRaises(AttributeError):
            m.foo = 2
        self.assertEqual(o.bar, 1)

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

    def test_not_null(self):
        class TestMapper(Mapper):
            foo = fields.Field('bar')
            baz = fields.Field('qux', null=True)

        o = SimpleNamespace(bar=1, qux=2)
        m = TestMapper(o)

        with self.assertRaises(ValueError):
            m.foo = None
        self.assertEqual(o.bar, 1)

        m.baz = None
        self.assertTrue(o.qux is None)

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

    def test_time_field(self):
        class TestMapper(Mapper):
            foo = fields.TimeField('bar')

        o = SimpleNamespace(bar=datetime.time(11, 51))
        m = TestMapper(o)

        self.assertEqual(m.foo, '11:51:00')

        m.foo = '6:32:00'
        self.assertEqual(o.bar, datetime.time(6, 32))

        now = datetime.datetime.now().time()

        m.foo = now
        self.assertEqual(o.bar, now)

    def test_date_field(self):
        class TestMapper(Mapper):
            foo = fields.DateField('bar')

        o = SimpleNamespace(bar=datetime.date(2012, 11, 21))
        m = TestMapper(o)

        self.assertEqual(m.foo, '2012-11-21')

        m.foo = '1975-05-11'
        self.assertEqual(o.bar, datetime.date(1975, 5, 11))

        today = datetime.date.today()

        m.foo = today
        self.assertEqual(o.bar, today)

    def test_datetime_field(self):
        class TestMapper(Mapper):
            foo = fields.DateTimeField('bar')

        o = SimpleNamespace(bar=datetime.datetime(2012, 11, 21, 16, 25, 9))
        m = TestMapper(o)

        self.assertEqual(m.foo, '2012-11-21 16:25:09')

        m.foo = '1975-05-11 09:35:01'
        self.assertEqual(o.bar, datetime.datetime(1975, 5, 11, 9, 35, 1))

        now = datetime.datetime.now()

        m.foo = now
        self.assertEqual(o.bar, now)

    def test_context_field(self):
        class M(Mapper):
            @fields.context_field
            def scaled(self, obj):
                return obj.value * self._context['factor']

            @scaled.setter
            def scaled(self, obj, value):
                obj.value = value // self._context['factor']

        o = SimpleNamespace(value=1)
        m = M(o, factor=10)

        self.assertEqual(m.scaled, 10)
        m.scaled = 20
        self.assertEqual(o.value, 2)
