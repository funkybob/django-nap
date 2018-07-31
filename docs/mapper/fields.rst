======
Fields
======

The `field` decorator
---------------------

The `field` decorator works exactly like `property`, however it will operate on
the "bound" object, not the Mapper.

.. class:: field()

   :param required: Is this field required? Default: True
   :param default: The value to use if the source value is absent. May be a
                   callable that takes no arguments.
   :param readonly: Can the field be updated? Default: True
   :param null: Is None a valid valie? Default: False

The decorator can be used bare, or with arguments:

.. code-block:: python

    class M(Mapper):

        @mapper.field
        def foo(self):
            return self.bar

        @mapper.field(default=0)
        def baz(self):
            return self.qux

        @baz.setter
        def baz(self, value):
            self.qux = value

As you can see, both the getter and setter of a `field` are defined the same
way as with `property`.

Basic fields
------------

For simple cases where the descriptor protocol is overkill, there is the
`Field` class.

.. class:: Field(...)

   :param attr: The name of the attribute on the bound object it gets/sets.
   :param required: Is this field required? Default: True
   :param default: The value to use if the source value is absent.
   :param readonly: Can the field be updated? Default: True
   :param null: Is None a valid valie? Default: False

.. code-block:: python

    class M(Mapper):
        foo = Field('bar')
        baz = Field('qux', default=0)

There are also typed fields:

- BooleanField
- IntegerField
- FloatField
- TimeField
- DateField
- DateTimeField

These will ensure the values stored are of the correct type, as well as being
presented to JSON in a usable format.

Accessing extra state
---------------------

Sometimes when serialising an object, you need to provide additional state.
This can be done using a ``context_field``, which subclasses ``field``, but
passes any extra ``kwargs`` that were pased to `Mapper` instance `context` to
the getter and setter methods as an extra argument.

.. class:: context_field()

   :param required: Is this field required? Default: True
   :param default: The value to use if the source value is absent.
   :param readonly: Can the field be updated? Default: True
   :param null: Is None a valid valie? Default: False

The following is an example from the test suite:

.. code-block:: python

   class M(Mapper):
       @fields.context_field
       def scaled(self, context):
           return self.value * context['factor']

       @scaled.setter
       def scaled(self, value, context):
           obj.value = value // self._context['factor']

   m = M(o, factor=10)

Accessing ``m.scaled`` will now return the value multiplied by 10.

------
Models
------

Relation Fields
---------------

To help with relations, the models module includes two extra field types:

- ToOneField
- ToManyField

Both accept the same extra arguments:

.. class:: RelatedField()

   :param model: The model this field relates to
   :param mapper: (Optional) the mapper to use to reduce instances.

When the mapper is omitted, only the Primary Key of the related model will be
used.

The ``ToManyField`` will work on any iterable, however if it's passed a
``Manager`` it will call ``.all()`` before iterating it. This makes it ideally
suited for ``ManyToMany`` and reverse ``ForeignKey`` accessors.
