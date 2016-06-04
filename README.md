django-nap
==========
[![Downloads](https://pypip.in/d/django-nap/badge.png)](https://crate.io/package/django-nap)
[![Version](https://pypip.in/v/django-nap/badge.png)](https://crate.io/package/django-nap)
[![Build Status](https://secure.travis-ci.org/funkybob/django-nap.png?branch=master)](http://travis-ci.org/funkybob/django-nap)

Read The Docs: http://django-nap.readthedocs.org/en/latest/

Change log: http://django-nap.readthedocs.org/en/latest/changelog.html

An API library for Django

A minimalist approach to object de/serialisers, RESTful views, and RPC views.

Benefits
========

1. Modular

    Unlike some tools, the Serialiser definition is separate from the API.

    This not only makes it easier to have different 'shapes' of data for
    different endpoints, but also allows using them in more places, not just
    your API.

1. Simple

    If you want an API that provides every feature ever, go look at Django REST
    Framework.  But if you want something simple and fast, this is your tool.

Overview
========

Installing
==========

It is NOT necessary to add nap to your INSTALLED\_APPS.  It does not provide
models, templates, template tags, or static files.

Currently, tests are only run in Python 2.7 and 3.3.  Except for the
DecimalField, all of the code should work on Python 2.6.

Django versions from 1.7 are supported.
