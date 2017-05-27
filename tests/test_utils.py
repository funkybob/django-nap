from types import SimpleNamespace

from django.test import SimpleTestCase

from nap.utils import ripper


class UtilsTestCase(SimpleTestCase):

    def test_ripper(self):
        R = ripper.Ripper('a', 'b', foo='c')
        o = SimpleNamespace(a=1, b='2', c='bar')
        d = R(o)

        self.assertEqual(d, {
            'a': 1,
            'b': '2',
            'foo': 'bar',
        })
