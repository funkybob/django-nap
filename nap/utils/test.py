import json

from django.test import Client, TestCase


class JsonClient(Client):

    def generic(self, method, path, data='', *args, **kwargs):
        if 'json' in kwargs:
            if data:
                raise ValueError("Must specify at most one of 'data' and 'json'.")
            data = json.dumps(kwargs.pop('json'))
            kwargs.setdefault('content_type', 'text/json')
        return super(Client, self).generic(method, path, data, *args, **kwargs)


class ApiTestCase(TestCase):

    def assertResponseCode(self, url, status_code, method='get', **kwargs):
        result = self.client.generic(method, **kwargs)
        self.assertEqual(result.status_code, status_code)
        return result
