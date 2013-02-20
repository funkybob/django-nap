
HTTP Utilities
==============

In nap.http is a set of tools to go one step further than Django's existing HttpResponse.

## Status

Firstly, there is STATUS_CODES, which is a list of two-tuples of HTTP Status codes and their descriptions.

Also, and more usefully, there is the STATUS object.  Accessing it as a dict, you can look up HTTP status code descriptions by code:

    >>> STATUS[401]
    'Unauthorized'

However, you can also look up attributes to find out the status code:

    >>> STATUS.UNAUTHORIZED
    401

This lets it act as a two-way constant.

BaseHttpResponse
================

This class blends Django's HttpResponse with Python's Exception.  Why?  Because then, when you're nested who-knows how deep in your code, it can raise a response, instead of having to return one and hope everyone bubbles it all the way up.

    BaseHttpResponse
    +---HttpResponseSuccess
    |   |
    |   +---OK
    |   |
    |   +---Created
    |   |
    |   +---Accepted
    |   |
    |   +---NoContent
    |   |
    |   +---ResetContent
    |   |
    |   +---PartialContent
    |
    +---HttpResponseRedirect
    |   |
    |   +---MultipleChoices
    |   |
    |   +---MovedPermanently
    |   |
    |   +---Found
    |   |
    |   +---SeeOther
    |   |
    |   +---NotModified

It will be clear that, unlike Django, these mostly do not start with HttpResponse.  This is a personal preference, in that typically you'd use:

    from nap import http

    ...

        return http.Accept(...)


