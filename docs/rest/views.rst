=================
Class-Based Views
=================

Also included are some mixins for working with Django's Class-Based Views.

At a minimum, all of the following mixins require being mixed in to Django's base View.


Base Classes
============

.. class:: MapperMixin

   All of the following classes are based on this.

   .. attribute:: mapper_class

      You must set this to the :class:`DataMapper` to use when processing requests and responses.


List Classes
============

.. class:: ListMixin

   Base list mixin, extends Django's MultipleObjectMixin.

.. class:: ListGetMixin

   Provides ``get()`` for lists.

.. class:: ListPostMixin

   Provides ``post()`` for lists.


Single Object Classes
=====================

.. class:: ObjectMixin

   Base single object mixin, extends Django's SingleObjectMixin.

.. class:: ObjectGetMixin

   Provides ``get()`` for single objects.

.. class:: ObjectPutMixin

   Provides ``put()`` for single objects.

.. class:: ObjectPatchMixin

   Provides ``patch()`` for single objects.

.. class:: ObjectDeleteMixin

   Provides ``delete()`` for single objects.


Example
-------

Sample ``views.py`` that provides ``GET``, ``PUT``, ``PATCH``, and ``DELETE`` methods for the Poll model:

.. code-block:: python

   from django.views.generic import View

   from nap.datamapper.models import ModelDataMapper
   from nap.rest.views import ObjectGetMixin, ObjectPutMixin, ObjectPatchMixin, ObjectDeleteMixin, ObjectMixin

   from .models import Poll


   class PollMapper(ModelDataMapper):
       class Meta:
           model = Poll
           fields = ['question', 'pub_date']


   class SinglePollView(ObjectGetMixin, ObjectPutMixin, ObjectPatchMixin, ObjectDeleteMixin, ObjectMixin, View):
       model = Poll
       mapper_class = PollMapper
