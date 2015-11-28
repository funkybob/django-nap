ModelDataMappers
================

A ModelDataMapper will automatically create a DataMapper for a Django model. A
ModelDataMapper behaves very similar to a Django ModelForm, you use it by
setting some fields in an inner Meta class.

The fields that can be set are:

.. class:: ModelDataMapper

    .. attribute:: model

      Default: None
      The model this ``DataMapper`` is for

    .. attribute:: fields

      Default: []
      The list of fields to use. You can set it to '__all__' to map all fields.

    .. attribute:: exclude

      Default: []
      The list of fields to exclude from the Model

    .. attribute:: required

      Default: {}
      The list of overrides of default required values for fields inferred from
      the model.  It does not influence @field declarations.

You can rewrite the DataMapper so that it subclasses ModelDataMapper. Here's a
new Person object that subclasses Django's models.Model:

.. code-block:: python

    from django.db import models


    # An Django models.Model we want to create a DataMapper for
    class Person(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        is_alive = models.BooleanField(default=True)

Here is the PersonMapper rewritten to use a ModelDataMapper:

.. code-block:: python

    from nap import datamapper

    # This should reference the model package where we define Person
    from . import models


    class PersonMapper(datamapper.ModelDataMapper):
        class Meta:
            model = models.Person
            fields = '__all__'

You can still use the `property` built-in to get/set properties and fields on
a ModelDataMapper. This is useful when the model contains some properties that
the ModelDataMapper cannot understand, or when you want to customise how
certain fields are represented.

To illustrate this we will add a new Django field (models.UUIDField) to our
model. UUIDField does not have a filter built in to nap, so you will need to
define your own get and set functionality using the `field` decorator.

Here is a Person model object with a UUIDField:

.. code-block:: python

    from django.db import models


    # An Django models.Model we want to create a DataMapper for
    class Person(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        is_alive = models.BooleanField(default=True)
        uuid = models.UUIDField(default=uuid.uuid4, editable=False)

And here is a complete ModelDataMapper that will correctly handle this new type
of field:

.. code-block:: python

    from nap import datamapper

    from . import models


    class PersonMapper(datamapper.ModelDataMapper):
        class Meta:
            model = models.Person
            fields = '__all__'
            # We're defining uuid ourselves and don't want it auto-mapped.
            exclude = ['uuid']

        @datamapper.field
        def uuid(self):
            return str(self.uuid) # Remember: self refers to the bound object.