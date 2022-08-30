==============
HTTP Utilities
==============

In nap.http is a set of tools to go one step further than Django's existing
HttpResponse.

Status
======

Firstly, there is STATUS_CODES, which is a list of two-tuples of HTTP Status
codes and their descriptions.

Also, and more usefully, there is the STATUS object.  Accessing it as a dict,
you can look up HTTP status code descriptions by code:

.. code-block:: python

    >>> STATUS[401]
    'Unauthorized'

However, you can also look up attributes to find out the status code:

.. code-block:: python

    >>> STATUS.UNAUTHORIZED
    401

This lets it act as a two-way constant.

BaseHttpResponse
================

This class blends Django's HttpResponse with Python's Exception.  Why?  Because
then, when you're nested who-knows how deep in your code, it can raise a
response, instead of having to return one and hope everyone bubbles it all the
way up.

- BaseHttpResponse

  - HttpResponseSuccess

    - OK
    - Created
    - Accepted
    - NoContent
    - ResetContent
    - PartialContent

  - HttpResponseRedirect

    - MultipleChoices
    - MovedPermanently*
    - Found*
    - SeeOther*
    - NotModified
    - UseProxy*
    - TemporaryRedirect
    - PermanentRedirect

    Items marked with a * require a location passed as their first argument.
    It will be set as the ``Location`` header in the response.

  - HttpResponseError

    A common base class for all Error responses (4xx and 5xx)

  - HttpResponseClientError(HttpResponseError)

    - BadRequest
    - Unauthorized
    - PaymentRequired
    - Forbidden
    - NotFound
    - MethodNotAllowed
    - NotAcceptable
    - ProxyAuthenticationRequired
    - RequestTimeout
    - Conflict
    - Gone
    - LengthRequired
    - PreconditionFailed
    - RequestEntityTooLarge
    - RequestURITooLong
    - UnsupportedMediaType
    - RequestedRangeNotSatisfiable
    - ExpectationFailed

  - HttpResponseServerError(HttpResponseError)

    - InternalServerError
    - NotImplemented
    - BadGateway
    - ServiceUnavailable
    - GatewayTimeout
    - HttpVersiontNotSupported

It will be clear that, unlike Django, these mostly do not start with
HttpResponse.  This is a personal preference, in that typically you'd use:

.. code-block:: python

    from nap import http

    ...
        return http.Accept(...)

except_response
---------------

In case you want to use these raisable responses in your own views, Nap
provides a `except_response` decorator.

.. code-block:: python

    from nap.http.decorators import except_response

    @except_response
    def myview(request):
        try:
            obj = Thing.objects.get(user=request.user)
        except:
            raise http.BadRequest()
        return render(...)

The decorator will catch any `http.BaseHttpResponse` exceptions and return them
as the views response.

Http404 versus http.NotFound
============================

Generally in your API, you'll want to prefer http.NotFound for returning a 404
response.  This avoids being caught by the normal 404 handling, so it won't
invoke your handler404.
