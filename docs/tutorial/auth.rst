=============
Authorisation
=============

Because ``django-nap`` uses Django compatible Class-Based Views, you can
simply use the same mixins provided by ``django.contrib.auth``.


Login Required
--------------

Here is an example of a view which only permits logged in users to get/post
Choices:

.. code-block:: python

    from django.contrib.auth.mixins import LoginRequiredMixin

    class ChoiceListView(ChoiceMixin,
                         LoginRequiredMixin,
                         views.ListGetMixin,
                         views.ListPostMixin,
                         views.ListBaseView):
        pass
