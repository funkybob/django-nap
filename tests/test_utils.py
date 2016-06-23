
from django.test import TestCase

from nap.utils import digattr


class DigattrTestCase(TestCase):

    def test_001_simple(self):

        data = {
            'a': 1,
            'b': [1, 2, 3],
            'c': lambda: 4,
            'd': {
                'a': 'test',
            },
        }

        self.assertEqual(digattr(data, 'a'), 1)
        self.assertEqual(digattr(data, 'b.2'), 3)
        self.assertEqual(digattr(data, 'c'), 4)
        self.assertEqual(digattr(data, 'd.a'), 'test')
        self.assertEqual(digattr(data, 'd.a.1'), 'e')
