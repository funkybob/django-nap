
from django.test import TestCase

from nap import fields

class SourceObj(object):
    def __init__(self):
        self.bool = True
        self.int = 1
        self.str = 'test'

class FieldTestCase(TestCase):
    '''
    Field cycles:
    deflate: digattr -> reduce -> data[name]
    inflate: data[name] -> restore -> dest[name]
    '''

    def setUp(self):
        self.src = SourceObj()
        self.dest = {}

    def test_001_boolean(self):
        field = fields.BooleanField()
        field.deflate('bool', self.src, self.dest)
        self.assertEqual(self.dest['bool'], self.src.bool)

        data = {}
        field.inflate('bool', self.dest, data)
        self.assertEqual(data['bool'], True)
