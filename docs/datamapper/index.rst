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

.. toctree::
   :maxdepth: 2

   fields
   filters
   methods
   models
   datamapper