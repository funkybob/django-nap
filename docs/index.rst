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

Whilst there are many existing RESTful API tools about, many of them are very complex, and [as I found] some are quite slow!

I wanted to take the solid serialising pattern from TastyPie, with the separation of roles of django-rest-framework, and include a Publisher API I developed some time ago.

Nap does not provide the wide range of features you see in tools like Django REST Framework and TastyPie, like rate limiting, token authentication, automatic UI, etc.  Instead, it provides a flexible framework that makes it easy to combine with other specialised apps.

Contents:

.. toctree::
   :maxdepth: 2

   serialiser
   fields
   publisher
   auth
   api
   models
   http
   newrelic
   examples
   changelog

Quick Start
===========

1. Create a Serialiser for your Model in serialisers.py

.. code-block:: python

    from nap import models
    from myapp.models import MyModel

    class MyModelSerialiser(models.ModelSerialiser):
        class Meta:
            model = MyModel
            exclude = ['user',]

2. Create a Publisher in publishers.py, and register it.

.. code-block:: python

    from nap import api, models
    from myapp.serialisers import MyModelSerialiser

    class MyModelPublisher(models.ModelPublisher):
        serialiser = MyModelSerialiser()

    api.register('api', MyModelPublisher)

3. Auto-discover publishers, and add your APIs to your URLs:

.. code-block:: python

    from nap import api

    api.autodiscover()

    urlpatterns('',
        (r'', include(api.patterns())
        ...
    )

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

