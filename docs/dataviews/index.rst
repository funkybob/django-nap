==========
Data Views
==========

DataViews provide a 'veiw' of your objects, must like database views.

They allow you to easily write proxy objects, primarily for converting between
serialised and live formats of your data.

DataViews work using Python's descriptor protocol, which is most commonly used
via the `property` built-in.

When constructing a DataView you can pass an object for it to "bind" to. All
field access to the DataView fields will proxy to this bound object.

.. toctree::
   :maxdepth: 2

   quickstart
   dataview
