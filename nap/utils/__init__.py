import json
from cgi import parse_header, parse_multipart
from inspect import isgenerator

from django.core.serializers.json import DjangoJSONEncoder
from django.http import QueryDict

from .. import http

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

        content_type, content_data = parse_header(self.request.META.get('CONTENT_TYPE', ''))

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
                return parse_multipart(self.request.body, content_data)

        return self.request.POST

    def loads(self, data, **kwargs):
        '''Serialise data for responses.'''
        kwargs.setdefault('cls', self.JSON_DECODER)
        return json.loads(data, **kwargs)


def flatten_errors(errors):
    '''
    Utility function to turn an ErrorDict into a dict of lists of strings.
    '''
    return {
        field: [
            error if isinstance(error, str) else (
                error.message % error.params if error.params else error.message
            )
            for error in errors
        ]
        for field, errors in errors.items()
    }


class List(list):
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
