from __future__ import unicode_literals
from django.test import TestCase

import json


class RPCTest(TestCase):

    def call(self, data=None, action='echo', content_type='application/json', **kwargs):
        if action is not None:
            kwargs['HTTP_X_RPC_ACTION'] = action
        if content_type is not None:
            kwargs['content_type'] = content_type
        if data is not None:
            kwargs['data'] = data
        return self.client.post('/rpc/', **kwargs)

    def test_body_omitted(self):
        r = self.call(None)
        self.assertEqual(r.content.decode('utf-8'), '{}')

    def test_body_not_json(self):
        r = self.call('this is not actually json')
        self.assertEqual(r.status_code, 400)

    def test_body_not_map(self):
        r = self.call('["this is a list rather than","a dictionary"]')
        self.assertEqual(r.status_code, 400)

    def test_body_not_string_keys(self):
        r = self.call('{"key":"value",42:"uh oh"}')
        self.assertEqual(r.status_code, 400)

    def test_basic(self):
        r = self.call(json.dumps({'foo': 'bar', 'baz': 42}))
        data = r.content.decode('utf-8')
        self.assertEqual(json.loads(data), {'foo': 'bar', 'baz': 42})

    def test_no_content_type(self):
        # Note of caution: when it does it as multipart/form-data in this way
        # (foo=bar), each value is taken as a list. May not be what's intended.
        r = self.call({"foo": "bar"}, content_type=None)
        data = r.content.decode('utf-8')
        self.assertEqual(json.loads(data), {'foo': ['bar']})

    def test_no_action(self):
        r = self.call(None, action=None)
        self.assertEqual(r.status_code, 405)

    def test_bad_action(self):
        r = self.call(None, action='bad')
        self.assertEqual(r.status_code, 412)
