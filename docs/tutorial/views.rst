=====
Views
=====

Now it's time to make our data visible to the outside world.

`django-nap` builds on Django's Class-Based Generic Views.

Question List
-------------

First, let's add our question list view.

.. code-block:: python
   :caption: polls/views.py

    from nap.rest import views

    from . import mappers, models

    class QuestionMixin:
        model = models.Question
        mapper_class = mappers.QuestionMapper


   class QuestionListView(QuestionMixin,
                          views.ListGetMixin,
                          views.BaseListView):
      pass

So, we've defined a common `QuestionMixin` class to help hold common
definitions for list and object views, and a `QuestionListView`.

This view is composed of our `QuestionMixin`, and two classes from
``django.nap.rest.views``: `ListGetMixin` and `BaeListView`

The `BaseListView` class provides common functionality for all list views,
including Django's `MultipleObjectMixin`.

The `ListGestMixin` adds a simple `get` method, which will return a list of
mapped instances of our model.
