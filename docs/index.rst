.. django-nap documentation master file, created by
   sphinx-quickstart on Thu Nov 28 11:22:05 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Take a REST with django-nap: APIs for Django
============================================

.. rubric:: Web APIs you can do in your sleep...

.. image:: https://travis-ci.org/funkybob/django-nap.png
           :target: https://secure.travis-ci.org/funkybob/django-nap.png?branch=master

In the spirit of the Unix philosophy, Nap provides a few tools which each do
one thing, and do it well.  They are:

1. Serialiser

   Declarative style Serialiser definitions for reducing complex Python objects
   to simple types expressible in JSON.

2. RESTful Publisher

   A Class-based view system which merges many related views into a single
   class, including url routing.

3. RESTful Class-Based Views

   A collection of mixins and views for building class-based API views.

4. RPC View

   A mixin for Django's class-based views which allows a single url to provide
   multiple RPC methods.

5. Data Mapper

   Alternative approach to converting objects between serialisable forms and
   program objects.

Nap does not provide the wide range of features you see in tools like Django
REST Framework, such as rate limiting, token authentication, automatic UI, etc.
Instead, it provides a flexible framework that makes it easy to combine with
other specialised apps.


.. toctree::
   :maxdepth: 2
   :caption: Table of Contents
   :name: mastertoc
   :titlesonly:

   quickstart
   serialiser/index
   datamapper/index
   rest/index
   rpc/index
   extras/index
   api/index
   testing
   tutorial/index
   examples
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

