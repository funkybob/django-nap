
Fields
======

Fields are declared on Serialisers to pluck values from the object.

In general, the basic Field class will suffice in most cases, however there are two special fields for including complex objects using another Serialiser class.

Field objects
=============

.. method:: Field.__init__([``attribute``=None,] [``default``=None,] [``readonly``=False])

    Defines a field which controls how values are converted from the object to its pre-serialised "reduced" form.


Attributes
----------


