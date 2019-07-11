import json
from cgi import FieldStorage
from inspect import isgenerator

from django.core.serializers.json import DjangoJSONEncoder
from django.http import QueryDict

from .. import http

# JSONDecodeError was added in Python 3.5
try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


class JsonMixin:
    '''
    Common methods for handling JSON request data.
    '''
    CONTENT_TYPES = ['application/json', 'text/json']
    JSON_DECODER = None

    def get_request_data(self, default=None):
        '''Retrieve data from request'''
        from django.conf import settings
        encoding = self.request.encoding or settings.DEFAULT_CHARSET

        content_type = self.request.content_type

        if content_type in self.CONTENT_TYPES:
            if not self.request.body:
                return default
            try:
                return self.loads(self.request.body.decode(encoding))
            except JSONDecodeError:
                raise http.BadRequest()

        if self.request.method in ('PUT', 'PATCH'):
            if content_type == 'application/x-www-form-urlencoded':
                return QueryDict(self.request.body, encoding=encoding)
            elif content_type == 'multipart/form-data':
                return FieldStorage(
                    self.request,
                    headers=self.request.META,
                    strict_parsing=True,
                    encoding=encoding,
                )

        return self.request.POST

    def loads(self, data, **kwargs):
        '''Serialise data for responses.'''
        kwargs.setdefault('cls', self.JSON_DECODER)
        return json.loads(data, **kwargs)


class List(list):
    '''
    A list-alike for generators to fool json.dump.
    '''
    def __init__(self, gen):
        self.gen = gen

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.gen)

    def __bool__(self):
        return True


class NapJSONEncoder(DjangoJSONEncoder):

    def default(self, o):
        if isgenerator(o):
            return List(o)
        m = getattr(o, '__json__', None)
        if callable(m):
            return m()
        return super().default(o)
