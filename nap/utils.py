from __future__ import unicode_literals

from cgi import parse_header
import json

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

    def get_request_data(self, default=None):
        '''Retrieve data from request'''
        c_type, _ = parse_header(self.request.META.get('CONTENT_TYPE', ''))
        if c_type in self.CONTENT_TYPES:
            if not self.request.body:
                return default
            return self.loads(self.request.body.decode(
                getattr(self.request, 'encoding', None) or ISO_8859_1
            ))
        return self.request.POST

    def dumps(self, data):
        '''How to parse content that matches our content types list.'''
        return json.dumps(data)

    def loads(self, data):
        '''Serialise data for responses.'''
        return json.loads(data)
