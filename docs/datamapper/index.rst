===========
DataMappers
===========

As the name suggests, a DataMapper will map properties on themselves to your 
object. They allow you to easily write proxy objects, primarily for converting 
between serialised (JSON) and live (Python) formats of your resources. They are 
an alternative approach to using Serialisers. 

.. Warning::
    Since a DataMapper instance retain a reference to the object they are bound 
    to, even when using << syntax, instances MUST NOT be shared between threads.

Field decorator: get/set
========================

You can set and get properties on a DataMapper by using Python's descriptor 
protocol, which allows you to control how properties are read from and written 
to your objects. This is most commonly implemented via the `property` built-in. 
When constructing a DataMapper you can pass an object for it to "bind" to. All 
field access to the DataMapper fields will proxy to this bound object. 

Here's an example to illustrate some of these concepts:

.. code-block:: python

    # An object we want to create a DataMapper for
    class Person(object):

        def __init__(self, first_name, last_name, age, is_alive):
            self.first_name = first_name
            self.last_name = last_name
            self.age = age
            self.is_alive = is_alive


    from nap import datamapper

    # A DataMapper that we are creating for the Person object
    class UserMapper(datamapper.DataMapper):

        '''
        The self argument refers to the object we bind the DataMapper to when 
        we construct it. It DOES NOT refer to the instance of the UserMapper.
        '''
        @datamapper.field 
        def name(self):
            return {}.format(self.first_name, self.last_name)

        # We can use the Field class for simpler cases
        first_name = datamapper.Field('first_name')
        last_name = datamapper.Field('last_name')
        is_alive = datamapper.Field('is_alive')

    # Construct instances of the Person and a DataMapper clases
    person = Person('Jane', 'Doe', 22, True)
    mapper = DataMapper(person)

The decorator `field` works exactly like `property`, however it will operate on 
the "bound" object, not the DataMapper. The Field class covers simpler cases, 
as well as allowing easier control. Field's first argument is the name of the 
property on the bound object it gets/sets.

Filters: validation and type casting
====================================
Filters provide casting and validation functions for Fields. That means you 
need to use them to: perform inbound field validation and to perform outbound
type casting. There are a number of filters built-in to nap:

- DateFilter
- TimeFilter 
- DateTimeFilter
- BooleanFilter
- IntegerFilter
- FloatFilter
- NotNullFilter

Here's a small example to show you how to use a BooleanFilter, which will 
ensure the values _set_ on the is_alive property are proper Booleans. When
filters fail a ValidationError is raised.

.. code-block:: python

    from nap import datamapper


    class UserMapper(datamapper.DataMapper):

        @datamapper.field 
        def name(self):
            return {}{}.format(self.first_name, self.last_name)

        first_name = datamapper.Field('first_name')
        last_name = datamapper.Field('last_name')
        is_alive = datamapper.Field('is_alive', filters=[BooleanFilter])

ModelDataMappers
================
A ModelDataMapper will automatically create a DataMapper for a Django model. A 
ModelDataMapper behaves very similar to a Django ModelForm, you use it by 
setting some fields in an inner Meta class. The fields that can be set are:

- model (default = None)
- fields (default = [])
- exclude (default = [])
- required (default = {})

``model`` will tell the ModelDataMapper which model class to create the mapping 
for. 

``fields`` contains a list of the fields we want the ModelDataMapper to 
automatically generate mappings for. There is a shortcut you can use and set 
fields = '__all__' to tell the ModelDataMapper to use all of the model fields.

``exclude`` is the compliment to fields, it tells the ModelDataMapper which of 
the fields to not create an automatic mapping for. 

``required`` dictionary is a list of overrides of the default calculated 
required values for fields

You can rewrite the DataMapper so that it subclasses ModelDataMapper. Here's a 
new Person object that subclasses Django's models.Model:

.. code-block:: python

    from django.db import models


    # An Django models.Model we want to create a DataMapper for
    class Person(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        age = models.IntegerField()
        is_alive = models.BooleanField(default=True)


Here is the UserMapper rewritten to use a ModelDataMapper:

.. code-block:: python

    from nap import datamapper

    # This should reference the model package where we define Person
    from . import models 


    class UserMapper(datamapper.ModelDataMapper):
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
        age = models.IntegerField()
        is_alive = models.BooleanField(default=True)
        uuid = models.UUIDField(default=uuid.uuid4, editable=False)

And here is a complete ModelDataMapper that will correctly handle this new type
of field:

.. code-block:: python

    from nap import datamapper

    from . import models 


    class UserMapper(datamapper.ModelDataMapper):
        class Meta:
            model = models.Person
            fields = '__all__'
            # We're defining uuid ourselves and don't want it auto-mapped.
            exclude = ['uuid']

        @datamapper.field
        def uuid(self):
            return str(self.uuid) # Remember: self refers to the bound object.

.. toctree::
   :maxdepth: 2

   datamapper
