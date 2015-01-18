.. django-nap documentation master file, created by
   sphinx-quickstart on Thu Nov 28 11:22:05 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Take a REST with django-nap: APIs for Django
============================================

.. rubric:: Web APIs you can do in your sleep...

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
REST Framework, such as rate limiting, token authentication, automatic UI, etc.
Instead, it provides a flexible framework that makes it easy to combine with
other specialised apps.

Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   serialiser/index
   serialiser/fields
   serialiser/models
   datamapper/index
   rest/index
   rpc/index
   extras/index
   api/index
   examples
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

