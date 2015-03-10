===========
Serialisers
===========

Serialisers define how to turn a Python object into a collection of JSON
compatible types, and back again.

They are defined using the familiar declarative syntax, like Models and Forms.

Serialiser objects
==================

A Serialiser class is defined much like a Form or Model, as a class with a list
of fields.

.. code-block:: python

    class MySerialiser(Serialiser):

        foo = fields.Field()
        bar = fields.Field('foo.bar')
        baz = fields.IntegerField()

Fields define what values will be output in the serialised format, their type,
and where to get them from the object being serialised.

Without an attribute specified, the field will use its name as the attribute name.

The Deflate Cycle
-----------------

For each declared field:

- Call the fields deflate method.  The field is expected to to store its result
  in the data dict.
- If there is a deflate_FOO method on the Serialiser, set the value in the data
  dict to its return value.

The Inflate Cycle
-----------------

For each declared field:

- If the Serialiser has an inflate_FOO method, its result is stored in the
  obj_data dict.
- Otherwise, call the fields inflate method.  The field is expected to store its
  result in the obj_data dict.
- If there were no ValidationError exceptions raised, pass the obj_data,
  instance, and kwargs to restore_object.

If any ValidationError exceptions are raised during inflation, a
ValidationErrors exception is raised, containing all the validation errors.

Custom Deflaters
----------------

.. method:: deflate_FOO(obj=obj, data=data, \**kwargs)

    After the ``Field``'s deflate method is called, if a matching deflate_FOO
    method exists on the class it will be passed the source object ``obj``, the
    updated data dict ``data``, and any additional keyword arguments as passed
    to ``object_deflate``.

    .. note::

       The custom deflate methods are called after all Field deflate methods
       have been called.

Custom Inflaters
----------------

.. method:: inflate_FOO(data, obj, instance, \**kwargs)

    If an inflate_FOO method exists on the class, it will be called instead of
    the ``Field``'s inflate method.  It is passed the source data, the inflated
    object data, the instance (which defaults to None), and any keyword
    arguments as passed to object_inflate.

    .. note::

       The custom inflate methods are called after all Field inflate methods
       have been called.

    The custom inflater may raise a ``nap.exceptions.ValidationException`` to
    indicate the data are invalid.
