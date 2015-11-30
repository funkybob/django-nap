=================
Class-Based Views
=================

Also included are some mixins for working with Django's Class-Based Generic
Views.  As they follow the existing CBV interfaces, they are compatible with
existing decorators and other utilities.

At their core is the `MapperMixin`, which extends the
`:class:JsonMixin <nap.utils.JsonMixin>`.  This provides ways to get the mapper
to use for the request, and utility functions for returning empty, single
object, and multiple object responses.

Additionally it provides wrappers for these to use specific response codes,
which can be configured on the class also.

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

      Returns a single response with ``self.created_status``.

   .. method:: deleted_response()

      Returns an empty response with ``self.deleted_status``.

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

.. class:: ObjectMixin(MapperMixin, SingleObjectMixin)

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

Sample ``views.py`` that provides ``GET``, ``PUT``, ``PATCH``, and ``DELETE``
methods for the Poll model:

.. code-block:: python

   from nap.datamapper.models import ModelDataMapper
   from nap.rest.views import (
       ObjectGetMixin, ObjectPutMixin, ObjectPatchMixin, ObjectDeleteMixin,
       BaseObjectView,
   )

   from .models import Poll


   class PollMapper(ModelDataMapper):
       class Meta:
           model = Poll
           fields = ['question', 'pub_date']


   class PollDetailView(ObjectGetMixin,
                        ObjectPutMixin,
                        ObjectPatchMixin,
                        ObjectDeleteMixin,
                        BaseObjectView):
       model = Poll
       mapper_class = PollMapper


Example: Updating two objects
-----------------------------

Here's an example of updating two related objects in a single PATCH call.

.. code-block:: python

   class UserDetailView(ObjectGetMixin, BaseObjectView):
        model = User
        mapper_class = UserMapper

        def patch(self, request, *args, **kwargs):
            data = self.get_request_data({})

            self.object = user = self.get_object()

            errors = {}

            mapper = self.get_mapper(user)
            try:
                data >> mapper # This is shorthand for _patch
            except ValidationError as e:
                errors.update(dict(e))

            profile_mapper = ProfileMapper(user.profile)
            try:
                data >> profile_mapper # This is shorthand for _patch
            except ValidationError as e:
                errors.update(dict(e))

            if errors:
                return self.patch_invalid(errors)

            user.save()
            user.profile.save()

            return self.ok_response(object=user, mapper=mapper)


Example: Customising GET 
------------------------

Here's an example of customising a GET call based on a querystring:

.. code-block:: python

   class QuestionListView(ListGetMixin, BaseListView):
        model = Question
        mapper_class = QuestionMapper

        def get(self, request, *args, **kwargs):
            qset = self.get_queryset()

            # Apply filtering to get only questions for a particular poll
            poll_id = request.GET.get('poll_id')
            if poll_id:
                qset = qset.filter(poll_id=poll_id)
                
            self.object_list = qset
            return self.ok_response(object_list=qset)