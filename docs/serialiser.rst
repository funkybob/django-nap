===========
Serialisers
===========

.. module: nap.serialiser
    :synopsis: Classes for serialising objects.

Quick Overview
==============

Serialisers define how to turn a Python object into a collection of JSON compatible types.

They are defined using the familiar declarative syntax, like Models and Forms.


Serialiser objects
==================

.. class:: Serialiser

    class MySerialiser(Serialiser):
        foo = Field()
        bar = Field('foo.bar')


