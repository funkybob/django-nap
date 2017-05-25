Quick Start
===========

Nap REST views work by combining Mappers with composible Class-Based Views.

Let's see how you might got about providng an API for the Poll example from the
Django tutorial.

Mapper/Views Quick Start
------------------------

1. Create a Mapper for your Model in mappers.py

This is very much like defining a ModelForm.

.. code-block:: python

    from nap import mapper

    from . import models


    class QuestionMapper(mapper.ModelMapper):
        class Meta:
            model = models.Question
            fields = '__all__'

2. Create some views in rest_views.py

.. code-block:: python

    from nap.rest import views

    from . import mappers, models

    class QuestionMixin:
        model = models.Question
        mapper_class = mappers.QuestionMapper


    class QuestionListView(QuestionMixin,
                           views.ListGetMixin,
                           views.ListPostMixin,
                           views.BaseListView):
        pass

    class QuestionObjectView(QuestionMixin,
                             views.ObjectGetMixin,
                             views.ObjectPutMixin,
                             views.BaseObjectView):
        pass

The `BaseListView` provides the core of any object list view, deriving from
Django's `MultipleObjectMixin`.  Then we mix in the default handlers for
``GET`` and ``POST`` actions.

Similarly, the `BaseObjectView` supports single object access, deriving from
Django's `SingleObjectMixin`.

Where the list view has ``POST`` to create a new record, the object view has
``PUT`` to update an existing record.

3. Add your APIs to your URLs:

.. code-block:: python

    urlpatterns = [
        url(r'^question/$',
            QuestionListView.as_view(),
            name='question-list'),

        url(r'^question/(?P<pk>\d+)/$',
            QuestionObjectView.as_view(),
            name='question-detail'),
    ]

And we're done.  You can how access your Question model!
