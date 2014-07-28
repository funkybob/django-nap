=============
Model Classes
=============

Just as there is ModelForm for Forms, there is ModelSerialiser for Serialiser.

ModelSerialiser
===============

This class will inspect a Model and generate appropriate fields for it.

.. code-block:: python

    class MyModelSerialiser(ModelSerialiser):

        class Meta:
            model = MyModel
            fields = [...fields to include...]
            exclude = [...fields to exclude...]
            read_only = [...fields to mark read-only...]

Like any other serialiser, you can define additional fields, as well as custom
inflate/deflate methods.

By default, the ``restore_object`` method will pass the inflated dict to the
model to create a new instance, or update all the properties on an existing
instance.  It will save the updated instance, however you can pass commit=False
to prevent this.


Meta
----

The ``ModelSerialiser`` supports additional ``Meta`` properties:

.. class:: ModelMeta

   .. attribute:: model

      Default: None
      The model this ``Serialiser`` is for

   .. attribute:: fields

      Default: ()
      The list of fields to use from the Model

   .. attribute:: exclude

      Default: ()
      The list of fields to ignore from the Model

   .. attribute:: read_only_fields

      Default: ()
      The list of fields from the Model to mark as read-only

   .. attribute:: field_types

      Default {}
      A map of field names to Field class overrides.

   .. attribute:: related_fields

      Default: ()

   .. attribute:: ignore_fields

      Default: ()
      When restoring an object, the fields which should not be passed to the
      instance.

   .. attribute:: key_fields

      Default: ('id',)
      When trying to ``get_or_create`` a model instance, which fields from the
      inflated data should be used to match the model.

   .. attribute:: defaults

      Default: {}
      When trying to ``get_or_create`` a model instance, additional default
      values to pass.

   .. attribute:: core_fields

      Default: ()
      When trying to ``get_or_create`` a model instance, additional fields to
      include in the defaults dict.


There are two extra sub-classes to help building complex cases when restoring
instances.

ModelReadSerialiser will only retrieve existing instances, passing all data to
the managers ``get`` method.

The ModelCreateUpdateSerialier will try to construct a new instance, or update
an existing one if it can be found.

The values found from ``Meta.key_fields`` will be passed to ``get_or_create``.
The ``defaults`` argument will be constructed from ``Meta.defaults``, and the
infalted values listed in ``Meta.core_fields``.

Then, the instance will be updated for all fields not listed in
``Meta.related_fields`` or ``Meta.ignored_fields``.

Finally, all ``Meta.related_fields`` will be set by calling their ``add``
method.
