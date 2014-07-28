.. django-nap documentation master file, created by
   sphinx-quickstart on Thu Nov 28 11:22:05 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Take a REST with django-nap: APIs for Django
============================================

.. image:: https://travis-ci.org/funkybob/django-nap.png
           :target: https://secure.travis-ci.org/funkybob/django-nap.png?branch=master

.. image:: https://pypip.in/d/django-nap/badge.png
           :target: https://crate.io/packages/django-nap

.. image:: https://pypip.in/v/django-nap/badge.png
           :target: https://crate.io/packages/django-nap

In the spirit of the Unix philosophy, Nap provides a few tools which each do one thing, and do it well.  They are:

1. Serialiser

   Declarative style Serialiser definitions for reducing complex Python objects
   to simple types expressible in JSON.

2. RESTful Publisher

   A Class-based view system which merges many related views into a single
   class, including url routing.

3. RPC Views

   A mixin for Django's class-based views which allows a single url to provide
   multiple RPC methods.

Nap does not provide the wide range of features you see in tools like Django
REST Framework and TastyPie, such as rate limiting, token authentication,
automatic UI, etc.  Instead, it provides a flexible framework that makes it
easy to combine with other specialised apps.

Contents:

.. toctree::
   :maxdepth: 2

   serialiser
   fields
   rest
   rpc
   http
   newrelic
   examples
   changelog

Quick Start
===========

1. Create a Serialiser for your Model in serialisers.py

.. code-block:: python

    from nap import rest
    from myapp.models import MyModel

    class MyModelSerialiser(rest.ModelSerialiser):
        class Meta:
            model = MyModel
            exclude = ['user',]

2. Create a Publisher in publishers.py, and register it.

.. code-block:: python

    from nap import rest
    from myapp.serialisers import MyModelSerialiser

    class MyModelPublisher(rest.ModelPublisher):
        serialiser = MyModelSerialiser()

    rest.api.register('api', MyModelPublisher)

3. Auto-discover publishers, and add your APIs to your URLs:

.. code-block:: python

    from nap import rest

    rest.api.autodiscover()

    urlpatterns('',
        (r'', include(rest.api.patterns())
        ...
    )

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

