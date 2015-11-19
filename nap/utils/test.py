import json

from django.test import Client, TestCase


class JsonClient(Client):

    def _massage(self, kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs.setdefault('content_type', 'application/json')
        return kwargs

    def get(self, *args, **kwargs):
        kwargs = self._massage(kwargs)
        return super(JsonClient, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs = self._massage(kwargs)
        return super(JsonClient, self).post(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs = self._massage(kwargs)
        return super(JsonClient, self).put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs = self._massage(kwargs)
        return super(JsonClient, self).delete(*args, **kwargs)


class ApiTestCase(TestCase):

    def assertResponseCode(self, url, status_code, method='get', **kwargs):
        result = getattr(self.client, method)(url, **kwargs)
        self.assertEqual(result.status_code, status_code)
        return result
