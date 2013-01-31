django-nap
==========
[![Build Status](https://secure.travis-ci.org/funkybob/django-nap.png?branch=master)](http://travis-ci.org/funkybob/django-nap)

A light REST library for Django.

Whilst there are many existing RESTful API tools about, many of them are very complex, and [as I found] some are quite slow!

I wanted to take the solid serialising pattern from TastyPie, with the separation of roles of django-rest-framework, and include a Publisher API I developed some time ago.

Benefits
========

Modular::
    By having the Serialiser as a separate class from the Publisher, it's simple to have different 'shapes' of data handled for different views.  You can also use the Serialisers elsewhere in your code.

Simple::
    If you want an API that provides every feature ever, go look at TastyPie.  But if you want something simple and fast, this is your tool.

Overview
========

Publisher
=========

A publisher gives you access to the resource.  Firstly, it uses the url patterns as follows:

    r'^object/(?P<object_id>\w+)/(?P<action>\w+)/?$'
    r'^object/(?P<object_id>\w+)/?$'
    r'^(?P<action>\w+)/?$'
    r'^$'

Requests are mapped to 'handlers', either list or object handlers.  A handler name is formed:

    {list|object}_{method}_{action}

In lieu of any action, 'default' is used.

Configuration properties:

    page_size
        If defined, lists will be paginated to fit this size.  Offsets will be adjusted to a page boundary.

Internal methods:

    get_serialiser():
        Return a Serialiser instance to use for this request.

    get_object_list():
        Return the full object list for this request.

    get_object(object_id):
        Return the instance with this ID.

    get_page(object_list):
        Returns the page of objects for this request.

    def get_data():
        Returns the client-supplied data.

Serialiser
==========

A serialiser defines how to convert an object to/from a JSON encodable format.

Serialisers are defined declaratively, using nap.field.Field instances

    class MySerialiser(Serialiser):
        foo = fields.Field()
        bar = fields.Field(readonly=True)
        baz = fields.Field('quux')
        fred = fields.Field('some.dotted.path')

With an instance of this class, you can deflate/inflate an instance of MyClass easily:

    ser = MySerialiser()
    data = ser.deflate(obj)
    updated_obj = ser.inflate(data, obj)

If you try to inflate without passing an object, a dummy 'object' instance will be created and have the values stored on it.

A field marked 'readonly' will not set its value on the object.

You can customise how a field is inflated by either sublcassing the Field class, or adding a ``deflate_FOO`` or ``inflate_FOO`` method.

    class BSerialiser(Serialiser):

        foo = fields.Field()

        def deflate_foo(self, obj, data, publisher=None):
            return obj.get_foo()

        def inflate_foo(self, data, obj, publisher=None):
            obj.set_foo(data['foo'])

There's also a ModelSerialiser, which will introspect for fields.

    class MySerialiser(ModelSerialiser):
        class Meta:
            model = MyModel

You can define extra fields on a ModelSerialiser, or override fields from the model.

Field Types
-----------

Besides Field, there are some special case fields also:

SerialiserField will accept a serialiser class to apply to the value retrieved.  Primarily, this is useful for providing values through a "ToOne" relation (OneToOne or ForeignKey), but can be used on any value, no matter how it's retrieved.

The ManySerialiserField will perform similarly, but will treat its value as an iterable.

