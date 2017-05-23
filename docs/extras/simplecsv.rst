Simple CSV
==========

A generator friendly, unicode aware CSV encoder class built for speed.

.. code-block:: python

    >>> csv = Writer(fields=['a', 'b', 'c'])
    >>> csv.write_headers()
    u'a,b,c\n'
    >>> csv.write([1, '2,', 'c'])
    u'1,"2,",c\n'


Options:

Seprator:

SEP = u','

Quote Character:

QUOTE = u'"'

What to replace a QUOTE in a field with

ESCQUOTE = QUOTE + QUOTE

What to put between records

LINEBREAK = u'\n'

ENCODING = 'utf-8'

