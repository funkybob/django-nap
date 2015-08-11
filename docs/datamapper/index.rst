============
Data Mappers
============

DataMappers, as the name suggest, map properties on themselves to your object.

They allow you to easily write proxy objects, primarily for converting between
serialised and live formats of your data.

DataMappers work using Python's descriptor protocol, which is most commonly
used via the `property` built-in.

When constructing a DataMapper you can pass an object for it to "bind" to. All
field access to the DataMapper fields will proxy to this bound object.

Thread Safety
=============

Since mapper instances retain a reference to the object they are bound to, even
when using << syntax, instances MUST NOT be shared between threads.

Quick Start
===========

.. code-block:: python

   from nap.datamapper import DataMapper, field, Field, BooleanFilter

   class UserMapper(DataMapper):
       @field
       def name(self):
           return self.get_full_name()
       name.required = False

       email = Field('email')
       is_staff = Field('is_staff', filters=[BooleanFilter])

In this simple example, we provide (name, email, is_staff) from a User model.

The simple decorator `field` works exactly like `property`, however it will
operate on the "bound" object, not the DataMapper.

The Field class covers simpler cases, as well as allowing easier control.  The
first argument is the name of the property on the bound object it gets/sets.

The `is_staff` field also has a filter to ensure values _set_ on this property are
proper bools.


.. toctree::
   :maxdepth: 2

   datamapper
