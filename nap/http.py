
'''Add some missing HttpResponse sub-classes'''
from django.http import *

from functools import partial

import json
import re

RESPONSE_CODES = (
    (100, 'Continue'),
    (101, 'Switching Protocols'),

    (200, 'OK'),
    (201, 'Created'),
    (202, 'Accepted'),
    #(203, Non-Authoritative Information),
    (204, 'No Content'),
    (205, 'Reset Content'),
    (206, 'Partial Content'),

    (300, 'Multiple Choices'),
    (301, 'Moved Permanently'),
    (302, 'Found'),
    (303, 'See Other'),
    (304, 'Not Modified'),
    (305, 'User Proxy'),
    #306 Deprecated
    (307, 'Temporary Redirect'),

    (400, 'Bad Request'),
    (401, 'Unauthorized'),
    (402, 'Payment Required'),
    (403, 'Forbidden'),
    (404, 'Not Found'),
    (405, 'Method Not Allowed'),
    (406, 'Not Acceptable'),
    (407, 'Proxy Autentication Required'),
    (408, 'Request Timeout'),
    (409, 'Conflict'),
    (410, 'Gone'),
    (411, 'Length Required'),
    (412, 'Precondition Failed'),
    (413, 'Request Entity Too Large'),
    (414, 'Request-URI Too Long'),
    (415, 'Unsupported Media Type'),
    (416, 'Requested Range Not Satisfiable'),
    (417, 'Expectation Failed'),

    (500, 'Internal Server Error'),
    (501, 'Not Implemented'),
    (502, 'Bad Gateway'),
    (503, 'Service Unavailable'),
    (504, 'Gateway Timeout'),
    (505, 'HTTP Version Not Supported'),
)

class ResponseTypes(object):
    def __init__(self, choices):
        self.choices = choices
        self._choices = dict(choices)
        for code, label in choices:
            setattr(self, re.sub('\W', '_', label.upper()), code)

    def __iter__(self):
        return iter(self.choices)

    def __getitem__(self, key):
        return self._choices[key]

RESPONSE = ResponseTypes(RESPONSE_CODES)

HttpResponseCreated = partial(HttpResponse, status=RESPONSE.CREATED)
HttpResponseAccepted = partial(HttpResponse, status=RESPONSE.ACCEPTED)
HttpResponseNoContent = partial(HttpResponse, status=RESPONSE.NO_CONTENT)
HttpResponseResetContent = partial(HttpResponse, status=RESPONSE.RESET_CONTENT)
HttpResponsePartialContent = partial(HttpResponse, status=RESPONSE.PARTIAL_CONTENT)

class JsonResponse(HttpResponse):
    '''Handy shortcut for dumping JSON data'''
    def __init__(self, content, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        super(JsonResponse, self).__init__(json.dumps(content), *args, **kwargs)
