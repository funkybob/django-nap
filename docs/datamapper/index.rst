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

.. toctree::
   :maxdepth: 2

   quickstart
   datamapper
