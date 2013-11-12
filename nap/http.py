from __future__ import unicode_literals

'''Add some missing HttpResponse sub-classes'''
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse, Http404
from django.utils.encoding import iri_to_uri

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

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
    (305, 'Use Proxy'),
    #306 Deprecated
    (307, 'Temporary Redirect'),
    (308, 'Permanent Redirect'),

    (400, 'Bad Request'),
    (401, 'Unauthorized'),
    (402, 'Payment Required'),
    (403, 'Forbidden'),
    (404, 'Not Found'),
    (405, 'Method Not Allowed'),
    (406, 'Not Acceptable'),
    (407, 'Proxy Authentication Required'),
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
            setattr(self, re.sub(r'\W', '_', label.upper()), code)

STATUS = ResponseTypes(STATUS_CODES)

class BaseHttpResponse(HttpResponse, Exception):
    '''
    A sub-class of HttpResponse that is also an Exception, allowing us to
    raise/catch it.

    With thanks to schinkel's repose.
    '''

#
# Success Responses (2xx)
#

class HttpResponseSuccess(BaseHttpResponse):
    '''A base class for all 2xx responses, so we can issubclass test.'''

class OK(HttpResponseSuccess):
    status_code = STATUS.OK

class Created(HttpResponseSuccess):
    status_code = STATUS.CREATED

class Accepted(HttpResponseSuccess):
    status_code = STATUS.ACCEPTED

class NoContent(HttpResponseSuccess):
    status_code = STATUS.NO_CONTENT

class ResetContent(HttpResponseSuccess):
    status_code = STATUS.RESET_CONTENT

class PartialContent(HttpResponseSuccess):
    status_code = STATUS.PARTIAL_CONTENT

#
# Redirection Responses (3xx)
#

class HttpResponseRedirection(BaseHttpResponse):
    '''A base class for all 3xx responses.'''

class LocationHeaderMixin(object):
    '''Many 3xx responses require a Location header'''
    def __init__(self, location, *args, **kwargs):
        super(LocationHeaderMixin, self).__init__(*args, **kwargs)
        parsed = urlparse(location)
        if parsed.scheme and parsed.scheme not in self.allowed_schemes:
            raise SuspiciousOperation(
                "Unsafe redirect to URL with protocol '%s'" % parsed.scheme
            )
        self['Location'] = iri_to_uri(location)

    url = property(lambda self: self['Location'])


class MultipleChoices(HttpResponseRedirection):
    status_code = STATUS.MULTIPLE_CHOICES

class MovedPermanently(LocationHeaderMixin, HttpResponseRedirection):
    status_code = STATUS.MOVED_PERMANENTLY

class Found(LocationHeaderMixin, HttpResponseRedirection):
    status_code = STATUS.FOUND

class SeeOther(LocationHeaderMixin, HttpResponseRedirection):
    status_code = STATUS.SEE_OTHER

class NotModified(HttpResponseRedirection):
    status_code = STATUS.NOT_MODIFIED

class UseProxy(LocationHeaderMixin, HttpResponseRedirection):
    status_code = STATUS.USE_PROXY

class TemporaryRedirect(HttpResponseRedirection):
    status_code = STATUS.TEMPORARY_REDIRECT

class PermanentRedirect(HttpResponseRedirection):
    status_code = STATUS.PERMANENT_REDIRECT

#
# Client Error Responses (4xx)
#

class HttpResponseError(BaseHttpResponse):
    '''A base class for all 4xx responses.'''

class BadRequest(HttpResponseError):
    status_code = STATUS.BAD_REQUEST

# XXX Auth-Realm ?
class Unauthorized(HttpResponseError):
    status_code = STATUS.UNAUTHORIZED

class PaymentRequired(HttpResponseError):
    status_code = STATUS.PAYMENT_REQUIRED

class Forbidden(HttpResponseError):
    status_code = STATUS.FORBIDDEN

class NotFound(HttpResponseError):
    status_code = STATUS.NOT_FOUND

class MethodNotAllowed(HttpResponseError):
    def __init__(self, permitted_methods, *args, **kwargs):
        super(MethodNotAllowed, self).__init__(*args, **kwargs)
        self['Allow'] = ', '.join(permitted_methods)

    status_code = STATUS.METHOD_NOT_ALLOWED

class NotAcceptable(HttpResponseError):
    status_code = STATUS.NOT_ACCEPTABLE

class ProxyAuthenticationRequired(HttpResponseError):
    status_code = STATUS.PROXY_AUTHENTICATION_REQUIRED

class RequestTimeout(HttpResponseError):
    status_code = STATUS.REQUEST_TIMEOUT

class Conflict(HttpResponseError):
    status_code = STATUS.CONFLICT

class Gone(HttpResponseError):
    status_code = STATUS.GONE

class LengthRequired(HttpResponseError):
    status_code = STATUS.LENGTH_REQUIRED

class PreconditionFailed(HttpResponseError):
    status_code = STATUS.PRECONDITION_FAILED

class RequestEntityTooLarge(HttpResponseError):
    status_code = STATUS.REQUEST_ENTITY_TOO_LARGE

class RequestURITooLong(HttpResponseError):
    status_code = STATUS.REQUEST_URI_TOO_LONG

class UnsupportedMediaType(HttpResponseError):
    status_code = STATUS.UNSUPPORTED_MEDIA_TYPE

class RequestedRangeNotSatisfiable(HttpResponseError):
    status_code = STATUS.REQUESTED_RANGE_NOT_SATISFIABLE

class ExpectationFailed(HttpResponseError):
    status_code = STATUS.EXPECTATION_FAILED

#
# Server Error (5xx)
#

class HttpResponseServerError(BaseHttpResponse):
    '''A base class for 5xx responses.'''

class InternalServerError(HttpResponseServerError):
    status_code = STATUS.INTERNAL_SERVER_ERROR

class NotImplemented(HttpResponseServerError):
    status_code = STATUS.NOT_IMPLEMENTED

class BadGateway(HttpResponseServerError):
    status_code = STATUS.BAD_GATEWAY

class ServiceUnavailable(HttpResponseServerError):
    status_code = STATUS.SERVICE_UNAVAILABLE

class GatewayTimeout(HttpResponseServerError):
    status_code = STATUS.GATEWAY_TIMEOUT

class HttpVersiontNotSupported(HttpResponseServerError):
    status_code = STATUS.HTTP_VERSION_NOT_SUPPORTED

#
# General Helpers
#

class JsonResponse(HttpResponse):
    '''Handy shortcut for dumping JSON data'''
    def __init__(self, content, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        super(JsonResponse, self).__init__(json.dumps(content), *args, **kwargs)
