=============
Model Classes
=============

Of course, there are classes to support dealing with Models.

ModelSerialiser
===============

This class will, like a ModelForm, inspect a Model and generate appropriate fields for it.

    class MyModelSerialiser(ModelSerialiser):

        class Meta:
            model = MyModel
            fields = [...fields to include...]
            exclude = [...fields to exclude...]
            read_only = [...fields to mark read-only...]

Like any other serialiser, you can define additional fields, as well as custom inflate/deflate methods.

By default, the restore_object method will pass the inflated dict to the model to create a new instance, or update all the properties on an existing instance.  By default, it will save the updated instance, however you can pass commit=False to prevent this.


ModelPublisher
==============

A ModelPublisher adds a model property to a publisher, which by default yields the model of the serialiser class.

It also adds get_object_list and get_object, where get_object assumes object_id is the pk of the model.

This gives basic read-only access to your model through the API.


modelserialiser_factory
=======================

This utility class allows you to programmatically generate a ModelSerialiser.

    myser = modelserialiser_factory(name, model, [fields=], [exclude=], [read_only=], \**kwargs)

The optional arguments will be treated the same as if passed in the Meta of a ModelSerialiser.  Additional deflate/inflate methods may be passed in kwargs.

ModelSerialiserField & ModelManySerialiserField
===============================================

Model counterparts to SerialiserField and ManySerialiserField.  If not passed a serialiser, they will generate one from the model provided.

