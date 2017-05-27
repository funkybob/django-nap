from django.test import TestCase, LiveServerTestCase

from nap.http import STATUS
from nap.rpc import client

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

    def test_options(self):
        r = self.client.options('/rpc/')
        self.assertEqual(r.status_code, STATUS.OK)
        data = json.loads(r.content.decode())
        self.assertTrue('echo' in data)

    def test_body_omitted(self):
        r = self.call(None)
        self.assertEqual(r.content.decode('utf-8'), '{}')

    def test_body_not_json(self):
        r = self.call('this is not actually json')
        self.assertEqual(r.status_code, STATUS.BAD_REQUEST)

    def test_body_not_map(self):
        r = self.call('["this is a list rather than","a dictionary"]')
        self.assertEqual(r.status_code, STATUS.BAD_REQUEST)

    def test_body_not_string_keys(self):
        r = self.call('{"key":"value",42:"uh oh"}')
        self.assertEqual(r.status_code, STATUS.BAD_REQUEST)

    def test_basic(self):
        r = self.call(json.dumps({'foo': 'bar', 'baz': 42}))
        data = json.loads(r.content.decode())
        self.assertEqual(data, {'foo': 'bar', 'baz': 42})

    def test_no_content_type(self):
        # Note of caution: when it does it as multipart/form-data in this way
        # (foo=bar), each value is taken as a list. May not be what's intended.
        r = self.call({"foo": "bar"}, content_type=None)
        data = json.loads(r.content.decode())
        self.assertEqual(data, {'foo': ['bar']})

    def test_no_action(self):
        r = self.call(None, action=None)
        self.assertEqual(r.status_code, STATUS.METHOD_NOT_ALLOWED)

    def test_bad_action(self):
        r = self.call(None, action='bad')
        self.assertEqual(r.status_code, STATUS.PRECONDITION_FAILED)


class RPCClientTest(LiveServerTestCase):

    def setUp(self):
        self.rpc = client.RPCClient('%s%s' % (self.live_server_url, '/rpc/'))

    def test_echo(self):
        resp = self.rpc.echo(foo='bar')
        self.assertEqual(resp, {'foo': 'bar'})
