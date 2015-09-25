from __future__ import unicode_literals

from cgi import parse_header, parse_multipart
import json

from django.utils import six
from django.utils.six.moves.urllib.parse import parse_qs

try:
    from django.core.handlers.wsgi import ISO_8859_1
except ImportError:  # pre-1.7
    ISO_8859_1 = str('iso-8859-1')


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


class JsonMixin(object):
    '''
    Common methods for handling JSON request data.
    '''
    CONTENT_TYPES = ['application/json', 'text/json']

    JSON_ENCODER = None
    JSON_DECODER = None

    def get_request_data(self, default=None):
        '''Retrieve data from request'''
        c_type, c_data = parse_header(self.request.META.get('CONTENT_TYPE', ''))

        if c_type in self.CONTENT_TYPES:
            if not self.request.body:
                return default
            return self.loads(self.request.body.decode(
                getattr(self.request, 'encoding', None) or ISO_8859_1
            ))

        if self.request.method in ('PUT', 'PATCH'):
            if c_type == 'application/x-www-form-urlencoded':
                return parse_qs(self.request.body)
            elif c_type == 'multipart/form-data':
                return parse_multipart(self.request.body, c_data)

        return self.request.POST

    def dumps(self, data):
        '''How to parse content that matches our content types list.'''
        return json.dumps(data, cls=self.JSON_ENCODER)

    def loads(self, data):
        '''Serialise data for responses.'''
        return json.loads(data, cls=self.JSON_DECODER)


def flatten_errors(errors):
    '''
    Utility function to turn an ErrorDict into a dict of lists of strings.
    '''
    return {
        field: [
            error if isinstance(error, six.string_types) else (
                error.message % error.params if error.params else error.message
            )
            for error in errors
        ]
        for field, errors in errors.items()
    }
