=================
Class-Based Views
=================

Also included are some mixins for working with Django's Class-Based Views.

At a minimum, all of the following mixins require being mixed in to Django's base View.


Base Classes
============

.. class:: MapperMixin

   All of the following classes are based on this.

   .. attribute:: response_class

      The class to construct responses from.

      Default: nap.http.JsonResponse

   .. attribute:: content_type

      The default content type for responses.

      Default: 'application/json'

   .. attribute:: mapper_class

      You must set this to the :class:`DataMapper` to use when processing
      requests and responses.

   .. attribute:: ok_status
      Default: nap.http.STATUS.ACCEPTED
   .. attribute:: accepted_status
      Default: nap.http.STATUS.CREATED
   .. attribute:: created_status
      Default: nap.http.STATUS.NO_CONTENT
   .. attribute:: error_status
      Default: nap.http.STATUS.BAD_REQUEST

      HTTP Status codes to use for different response types.

   .. method:: get_mapper(obj=None)

      Returns an instance of `mapper_class`

   .. method:: empty_response(\**kwargs)

      Returns an instance of `response_class` with no content.

   .. method:: single_response(\**kwargs)

      Return a response with a single object.

      Will use self.object if `object` is not passed.
      Will use self.mapper if `mapper` is not passed.

   .. method:: multiple_response(\**kwargs)

      Return a response with a list of objects.

      Will use self.object_list if 'object_list' is not passed.
      Will use self.mapper if `mapper` is not passed.

   .. method:: accepted_response()

      Returns an empty response with ``self.accepted_status``

   .. method:: created_response()
   .. method:: deleted_response()

      Returns a single response with the matching status.

   .. method:: error_response(error)

      Passes the supplied error dict through nap.utils.flatten_errors, and
      returns it with status=self.error_status

List Classes
============

.. class:: ListMixin(MapperMixin, MultipleObjectMixin)

   Base list mixin, extends Django's MultipleObjectMixin.

   .. method:: ok_response()

   Calls ``self.list_response(status=self.ok_response)``

.. class:: ListGetMixin

   Provides ``get()`` for lists.

.. class:: ListPostMixin

   Provides ``post()`` for lists.

   .. method:: post_invalid(errors)
   .. method:: post_valid()

.. class:: BaseListView(ListMixin, View)


Single Object Classes
=====================

.. class:: ObjectMixin

   Base single object mixin, extends Django's SingleObjectMixin.

   .. method:: ok_response()

      Calls self.single_response(status=self.ok_status)

.. class:: ObjectGetMixin

   Provides ``get()`` for single objects.

.. class:: ObjectPutMixin

   Provides ``put()`` for single objects.

   .. method:: put_valid()
   .. method:: put_invalid(errors)

.. class:: ObjectPatchMixin

   Provides ``patch()`` for single objects.

   .. method:: patch_valid()
   .. method:: patch_invalid(errors)

.. class:: ObjectDeleteMixin

   Provides ``delete()`` for single objects.

   .. method:: delete_valid()

.. class:: BaseObjectView(ObjectMixin, View)

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
