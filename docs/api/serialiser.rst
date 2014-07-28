==========
Serialiser
==========

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


