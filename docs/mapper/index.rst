===========
Mappers
===========

As the name suggests, a Mapper will map properties on themselves to your
object. They allow you to easily write proxy objects, primarily for converting
between serialised (JSON) and live (Python) formats of your resources.

.. Warning::
    Since a Mapper instance retain a reference to the object they are bound to,
    even when using << syntax, instances MUST NOT be shared between threads.


Field decorator: get/set
========================

Mappers work using Python's descriptor protocol, which is most commonly used
via the `property` built-in. This gives you full control over a Mapper's
properties. When constructing a Mapper you can pass an object for it to "bind"
to. All attribute access to the Mapper fields will proxy to this bound object.

Here's an example to illustrate some of these concepts:

.. code-block:: python

    # An object we want to create a Mapper for
    class Person:

        def __init__(self, first_name, last_name, is_alive):
            self.first_name = first_name
            self.last_name = last_name
            self.is_alive = is_alive


    from nap import mapper

    # A Mapper that we are creating for the Person object
    class PersonMapper(mapper.Mapper):
        '''
        The self argument refers to the object we bind the Mapper to when we
        construct it. It DOES NOT refer to the instance of the PersonMapper.
        '''
        @mapper.field
        def name(self):
            return '{}'.format(self.first_name, self.last_name)

        # We can use the Field class for simpler cases
        first_name = mapper.Field('first_name')
        last_name = mapper.Field('last_name')
        is_alive = mapper.Field('is_alive')

    # Construct instances of the Person and a Mapper classes
    person = Person('Jane', 'Doe', 22, True)
    mapper = PersonMapper(person)

The decorator `field` works exactly like `property`, however it will operate on
the "bound" object, not the Mapper. The Field class covers simpler cases, as
well as allowing easier control. Field's first argument is the name of the
property on the bound object it gets/sets.

Accessing extra state
---------------------

Sometimes when serialising an object, you need to provide additional state.
This can be done using a ``context_field``, which subclasses ``field`` and
additionally passes the `Mapper` instance to the getter and setter methos.

Any extra `kwargs` passed when the `Mapper` is instanciated are stored on the
instance in `self._context`.

Mapper Fields
=============

Mappers use the declarative syntax familiar from Django Models and Forms.

These are the valid supported types:

Field
-----

For simple cases where the descriptor protocol is overkill.

.. class:: Field(name, required=True, default=NOT_PROVIDED, filters=None)

   :param attr: The name of the attribute on the bound object it gets/sets.
   :param default: The value to use if the source value is absent.
   :param required: Is this field required? Default: True
   :param readonly: Can the field be updated? Default: True


DigField
--------

DigFields 'dig' out the value in a similar style to the dotted lookup syntax in
Django's templates

.. class:: DigField(instance, required=True, default=NOT_PROVIDED)

    :param instance: Reference to field on another instance using dot notation
    :param default: The value to use if the source value is absent.
    :param required: Is this field required? Default: True

MapperField
-----------

Used when serialising a model that has a foreign key relation.

.. class:: MapperField(mapper, required=True, default=NOT_PROVIDED)

    :param mapper: A Mapper that will serialise the field value.
    :param instance: Reference to a field on another instance using dot notation.
    :param default: The value to use if the source value is absent.


Mapper functions
================

A Mapper supports several methods:

``_reduce()`` will reduce the instance to its serialisable state, returning a
dict representation of the `Mapper`.

``_patch(data)`` will partially update (patch) a `Mapper`'s fields with the
values you pass in the data dict. If validation fails it will raise a
`ValidationError`.

``_apply(data)`` will fully update (put) a `Mapper`'s fields with the values
you pass in the data dict. If you don't pass a field in the data dict it will
try to set the field to the default value. If there is no default and the field
is required it will raise a `ValidationError`.

``_clean(data, full=True)`` is a hook for final pass validation. It allows you
to define your own custom cleaning code. You should update the ``self._errors``
dict. The ``full`` boolean indicates if the calling method was ``_apply``
(True) or ``_patch`` (False).

Here is some code to explain how these concepts work. We will continue to use
the Person class and PersonMapper class defined above.

Note that these methods only update the fields of the model instance. You will
need to call save() yourself to commit changes to the database.

Using _reduce:

.. code-block:: python

    p = Person('Jane', 'Doe', True)
    m = PersonMapper(p)
    reduced_p = m._reduce()
    print(reduced_p)

    # Output: {'first_name': 'Jane', 'last_name': 'Doe', 'is_alive': True}


Using _apply:

.. code-block:: python

    m = PersonMapper()
    m._apply({
        "first_name": "Jane",
        "last_name": "Doe",
        "is_alive": False
    })
    reduced = m.reduce()
    print(reduced)

    # Output: {'first_name': 'Jane', 'last_name': 'Doe', 'is_alive': False}


Using _patch:

.. code-block:: python

    p = Person('Jane', 'Doe', True)
    m = PersonMapper(p)
    m._patch({"last_name": "Notdoe"}) # This should patch last_name
    reduced = m.reduce()
    print(reduced)

    # Output: {'first_name': 'Jane', 'last_name': 'Notdoe', 'is_alive': True}

Using _clean:

.. code-block:: python

    class DeadPersonMapper(PersonMapper):
        def _clean(self):
            if self.is_alive:
                raise ValidationError("Only dead people accepted to the morgue.")

    m = DeadPersonMapper()
    m._apple({'last_name': 'Doe', 'first_name': 'John', 'is_alive': True})

    # ValidationError

Shortcuts
---------

As a convenience, Mappers support two shorthand syntaxes:

.. code-block:: python

   >>> data = mapper << obj

This will bind the mapper to the obj, and then call ``_reduce``.

.. code-block:: python

   >>> obj = data >> mapper

This will call ``_patch`` on the mapper, passing data, and returning the
updated object.

ModelMappers
============

A ModelMapper will automatically create a Mapper for a Django model. A
ModelMapper behaves very similar to a Django ModelForm, you control it by
setting some fields in an inner Meta class.

The fields that can be set are:

.. class:: ModelMapper

   .. attribute:: model

      Default: None
      The model this ``Mapper`` is for

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

   .. attribute:: readonly
      The list of fields which are read only.

      Must not conflict with `required`.

You can rewrite the Mapper so that it subclasses ModelMapper. Here's a new
Person object that subclasses Django's models.Model:

.. code-block:: python

    from django.db import models


    # An Django models.Model we want to create a Mapper for
    class Person(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        is_alive = models.BooleanField(default=True)

Here is the PersonMapper rewritten to use a ModelMapper:

.. code-block:: python

    from nap import mapper

    # This should reference the model package where we define Person
    from . import models


    class PersonMapper(mapper.ModelMapper):
        class Meta:
            model = models.Person
            fields = '__all__'

You can still use `field` to get/set properties and fields on a ModelMapper.
This is useful when the model contains some properties that the ModelMapper
cannot understand, or when you want to customise how certain fields are
represented.

To illustrate this we will add a new Django field (models.UUIDField) to our
model. UUIDField does not have a filter built in to nap, so you will need to
define your own get and set functionality using the `field` decorator.

Here is a Person model object with a UUIDField:

.. code-block:: python

    from django.db import models


    # An Django models.Model we want to create a Mapper for
    class Person(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        is_alive = models.BooleanField(default=True)
        uuid = models.UUIDField(default=uuid.uuid4, editable=False)

And here is a complete ModelMapper that will correctly handle this new type of
field:

.. code-block:: python

    from nap import mapper

    from . import models


    class PersonMapper(mapper.ModelMapper):
        class Meta:
            model = models.Person
            fields = '__all__'

        @mapper.field
        def uuid(self):
            return str(self.uuid) # Remember: self refers to the bound object.

.. toctree::
   :maxdepth: 2

   mapper