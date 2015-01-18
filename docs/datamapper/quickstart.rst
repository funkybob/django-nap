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
Additionally, it has a filter to ensure values _set_ on this property are
proper bools.
