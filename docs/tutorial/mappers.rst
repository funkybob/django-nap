=======
Mappers
=======

Mappers help us to convert our Python objects, like model instances, into
simpler type that are supported by JSON, and back again.

They help us map between how we want our data viewed in the API, and how it's
viewed by the rest of the system.

Mappers use a declarative style, just like Django's Models and Forms.

Also, just like Django Forms, there are ModelMappers to simplify building Mappers for models.

---------------
Question Mapper
---------------

So let's start with the `QuestionMapper`.  Create a new file in your poll/ app, and call it "mappers.py"

.. code-block:: python

    from nap import mapper

    from . import models


    class QuestionMapper(mapper.ModelMapper):
        class Meta:
            model = models.Question
            fields = '__all__'

For anyone familiar with ModelForms, this should look very familiar.

So what does this get us?  Well, let's drop into a shell and try it out.

.. code-block:: python

    >>> from polls.mappers import QuestionMapper
    >>> from polls.models import Question
    >>> q = Question.objects.first()
    >>> m = QuestionMapper(q)

So we can create a new instance of our mapper and "bind" it to our model
instance.

From now on, accessing attributes on the mapper instance will extract values
from that model instance.

.. code-block:: python

    >>> m.question_text
    "What's new?"
    >>> m.pub_date
    '2017-06-17 05:30:58+00:00'

Notice that the `pub_date` field came out as a string, in ISO-8601 format.

This works both ways.  We can set values on our model via the mapper:

.. code-block:: python

    >>> m.question_text = "So, what is new?"
    >>> q.question_text
    'So, what is new?'

There's also a helpful function to grab all the defined fields and return them as a dict:

.. code-block:: python

    >>> m._reduce()
    {'pub_date': '2017-06-17 05:30:58+00:00', 'question_text': "What's new?", 'id': 1}

The built in RESTful views in `django-nap` use this method to create JSON
serialisable data from your models.

Calculated Fields
-----------------

What if, as well as the publication date, we want to provide the age?

We can define mapper fields that do "work" as simply as we would add ``property`` to a class:

.. code-block:: python

    from django.utils import timezone


    class QuestionMapper(mapper.ModelMapper):
        class Meta:
            model = models.Question
            fields = '__all__'

    @mapper.field
    def age(self):
        return timezone.now() - self.pub_date

Of interest here is that the `self` passed to the getter function is not the
`QuestionMapper` class, but the object it is bound to - that is, our model
instance.

-------------
Choice Mapper
-------------

The `ChoiceMapper` is just as simple:

.. code-block:: python

    class ChoiceMapper(maper.ModelMapper):
        class Meta:
            model = models.Choice
            fields = '__all__'


-------
Updates
-------

Besides setting each field individually, `Mapper` provides two approaches to
updating your instance: ``_apply`` and ``_patch``. They update the instance
from a dict, as well as validate the data passed.

``_apply`` is used to update all the fields defined on the Mapper from a dict.
If a field on the mapper is marked as `required`, but is not provided in the
dict, this will be treated as an error.

Alternatively, ``_patch`` is used to update only the fields provided.

Any validation errors raised by fields will be gathered and passed in a single
ValidationError exception at the end of processing. The errors will also be
stored on the Mapper instance as ``_errors``.
