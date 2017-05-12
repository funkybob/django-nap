import json
from cgi import parse_header, parse_multipart

from django.http import QueryDict


def digattr(obj, attr, default=None):
    '''Perform template-style dotted lookup'''
    steps = attr.split('.')
    for step in steps:
        try:    # dict lookup
            obj = obj[step]
        except (TypeError, AttributeError, KeyError):
            try:    # attribute lookup
                obj = getattr(obj, step)
            except (TypeError, AttributeError):
                try:    # list index lookup
                    obj = obj[int(step)]
                except (IndexError, ValueError, KeyError, TypeError):
                    return default
        if callable(obj) and not getattr(obj, 'do_not_call_in_templates', False):
            obj = obj()
    return obj


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
            return self.loads(self.request.body.decode(encoding))

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
