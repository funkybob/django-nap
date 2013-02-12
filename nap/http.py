
'''Add some missing HttpResponse sub-classes'''
from django.http import *

from functools import partial

from collections import OrderedDict

import json
import re

STATUS_CODES = (
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

class ResponseTypes(OrderedDict):
    def __init__(self, choices):
        super(ResponseTypes, self).__init__(choices)
        for code, label in choices:
            setattr(self, re.sub('\W', '_', label.upper()), code)

STATUS = ResponseTypes(STATUS_CODES)

HttpResponseCreated = partial(HttpResponse, status=STATUS.CREATED)
HttpResponseAccepted = partial(HttpResponse, status=STATUS.ACCEPTED)
HttpResponseNoContent = partial(HttpResponse, status=STATUS.NO_CONTENT)
HttpResponseResetContent = partial(HttpResponse, status=STATUS.RESET_CONTENT)
HttpResponsePartialContent = partial(HttpResponse, status=STATUS.PARTIAL_CONTENT)

class JsonResponse(HttpResponse):
    '''Handy shortcut for dumping JSON data'''
    def __init__(self, content, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        super(JsonResponse, self).__init__(json.dumps(content), *args, **kwargs)
