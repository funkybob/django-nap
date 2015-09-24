from __future__ import unicode_literals

import json
import re

from django.core.exceptions import SuspiciousOperation
from django.http import Http404, HttpResponse  # NOQA
from django.utils.encoding import iri_to_uri
from django.utils.six.moves import http_client

'''Add some missing HttpResponse sub-classes'''

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


STATUS_CODES = list(http_client.responses.items()) + [
    (308, 'PERMANENT REDIRECT'),
    (427, 'BAD GEOLOCATION'),
]
STATUS_CODES = tuple(sorted(STATUS_CODES))

STATUS = OrderedDict(STATUS_CODES)
# Set constant-like properties for reverse lookup
for code, label in STATUS_CODES:
    setattr(STATUS, re.sub(r'\W', '_', label.upper()), code)


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


class BadGeolocation(HttpResponseError):
    status_code = STATUS.BAD_GEOLOCATION

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


try:
    from django.http import JsonResponse
except ImportError:
    # Back-ported from Django 1.7
    from django.core.serializers.json import DjangoJSONEncoder

    class JsonResponse(HttpResponse):
        """
        An HTTP response class that consumes data to be serialized to JSON.

        :param data: Data to be dumped into json. By default only ``dict`` objects
          are allowed to be passed due to a security flaw before EcmaScript 5. See
          the ``safe`` parameter for more information.
        :param encoder: Should be an json encoder class. Defaults to
          ``django.core.serializers.json.DjangoJSONEncoder``.
        :param safe: Controls if only ``dict`` objects may be serialized. Defaults
          to ``True``.
        """

        def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
            if safe and not isinstance(data, dict):
                raise TypeError('In order to allow non-dict objects to be '
                                'serialized set the safe parameter to False')
            kwargs.setdefault('content_type', 'application/json')
            data = json.dumps(data, cls=encoder)
            super(JsonResponse, self).__init__(content=data, **kwargs)
