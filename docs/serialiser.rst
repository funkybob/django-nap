===========
Serialisers
===========

Quick Overview
==============

Serialisers define how to turn a Python object into a collection of JSON
compatible types.

They are defined using the familiar declarative syntax, like Models and Forms.


Serialiser objects
==================

A Serialiser class is defined much like a Form or Model:

.. code-block:: python

    class MySerialiser(Serialiser):

        foo = fields.Field()
        bar = fields.Field('foo.bar')
        baz = fields.IntegerField()

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

For reach declared field:

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

Serialiser API
==============

.. class:: Serialiser()

   .. method:: object_deflate(obj, \**kwargs)

      Returns `obj` reduced to its serialisable format.

      The kwargs are passed on to field and custom deflate methods.

   .. method:: list_deflate(obj_list, \**kwargs)

      Return a list made by calling object_deflate on each item in the supplied
      iterable.

      Passes kwargs to each call to object_deflate.

   .. method:: object_inflate(data, instance=None, \**kwargs)

      Restore data to an object.  If the instance is passed, it is expected to
      be updated by ``restore_object``.

   .. method:: restore_object(obj_data, \**kwargs)

      Construct an object from the inflated data.

      By default, if Serialiser.obj_class has been provided, it will construct a
      new instance, passing objdata as keyword arguments.  Otherwise, it will
      raise a NotImplementedError.

