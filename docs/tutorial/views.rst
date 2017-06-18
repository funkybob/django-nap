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

The `ListGetMixin` adds a simple `get` method, which will return a list of
mapped instances of our model.

Let's add our new view to the existing ones, but with a 'api/' prefix:

.. code-block:: python
   :caption: urls.py

   from django.conf.urls import url

   from . import views

   urlpatterns = [
       # ex: /polls/
       url(r'^$', views.index, name='index'),
       # ex: /polls/5/
       url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
       # ex: /polls/5/results/
       url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
       # ex: /polls/5/vote/
       url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

       url(r'^api/', include([
         url(r'question/$', views.QuestionListView.as_view()),
       ]))
   ]

So we can now access our list of Questions at http://localhot:8000/api/question/ and should see something like this:

.. code-block:: json

   [
      {
         "id": 1,
         "question_text": "What's new?",
         "pub_date": "2017-06-17 05:30:58+00:00",
         "age": "20\u00a0hours, 15\u00a0minutes"
      }
   ]

--------------
Nested Records
--------------

That's great, but a Question with no Choices isn't much use, is it?

We can ask our mapper to render a list of related records using a `ToMany` field:

.. code-block:: python
   :caption: polls/mappers.py

   class QuestionMapper(mapper.ModelMapper):
      class Meta:
           model = models.Question
           fields = '__all__'

      @mapper.field
      def age(self):
           return timesince(self.pub_date)

      choices = mapper.ToManyField('choice_set')

The `ToManyField` will check if its value is a ``django.db.models.Manager``,
and call `.all()` on it if it is.

And now out output will look something like this:

.. code-block:: json

   [
      {
         "id": 1,
         "age": "20\u00a0hours, 19\u00a0minutes",
         "question_text": "What's new?",
         "pub_date": "2017-06-17 05:30:58+00:00",
         "choices": [1, 2]
      }
   ]

By default, a `ToManyField` will only render the primary keys of the related
objects. If you want to control how it's serialised, just specify a mapper on
the field.

.. code-block:: python
   :caption: polls/mappers.py

   choices = mapper.ToManyField('choice_set', mapper=ChoiceMapper)

Which will give us this output:

.. code-block:: json

   [
      {
         "pub_date": "2017-06-17 05:30:58+00:00",
         "age": "20\u00a0hours, 22\u00a0minutes",
         "question_text": "What's new?",
         "id": 1,
         "choices": [
            {
               "question": 1,
               "choice_text": "First Choice",
               "id": 1,
               "votes": 0
            },
            {
               "question": 1,
               "choice_text": "Another Choice",
               "id": 2,
               "votes": 0
            }
         ]
      }
   ]

We really don't need the question ID embedded there, so let's define a new choice mapper which will exclude that.

.. code-block:: python
   :caption: polls/mappers.py

    class InlineChoiceMapper(mapper.ModelMapper):
        class Meta:
            model = models.Choice
            fields = '__all__'
            exclude = ('question',)

And finally we see:

.. code-block:: json

   [
      {
         "choices": [
            {
               "votes": 0,
               "id": 1,
               "choice_text": "First Choice"
            },
            {
               "votes": 0,
               "id": 2,
               "choice_text": "Another Choice"
            }
         ],
         "question_text": "What's new?",
         "age": "20\u00a0hours, 27\u00a0minutes",
         "pub_date": "2017-06-17 05:30:58+00:00",
         "id": 1
      }
   ]
