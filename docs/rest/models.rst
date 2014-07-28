==============
ModelPublisher
==============

A ModelPublisher adds a model property to a publisher, which by default yields
the model of the serialiser class.

It also adds ``get_object_list`` and ``get_object``, where ``get_object``
assumes object_id is the pk of the model.

This gives basic read-only access to your model through the API.

modelserialiser_factory
=======================

This utility class allows you to programmatically generate a ModelSerialiser.

.. code-block:: python

    myser = modelserialiser_factory(name, model, [fields=], [exclude=], [read_only=], **kwargs)

The optional arguments will be treated the same as if passed in the Meta of a
ModelSerialiser.  Additional deflate/inflate methods may be passed in kwargs.

ModelSerialiserField & ModelManySerialiserField
===============================================

Model counterparts to SerialiserField and ManySerialiserField.  If not passed a
serialiser, they will generate one from the model provided.

