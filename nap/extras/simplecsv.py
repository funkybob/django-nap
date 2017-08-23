
class Writer:
    '''
    A generator friendly, unicode aware CSV encoder class built for speed.

    >>> csv = Writer(fields=['a', 'b', 'c'])
    >>> csv.write_headers()
    b'a,b,c\n'
    >>> csv.write([1, '2,', 'c'])
    b'1,"2,",c\n'

    '''
    __slots__ = ('fields', 'headers', 'SEP', 'QUOTE', 'ESCQUOTE', 'LINEBREAK', 'ENCODING', 'escape_field')

    def __init__(self, fields,
                 headers=None,
                 SEP = u',',                # What to put between fields
                 QUOTE = u'"',              # What to wrap fields in, if they contain SEP
                 ESCQUOTE = None,           # What to replace a QUOTE in a field with
                 LINEBREAK = u'\n',         # What to put between records
                 ENCODING = 'utf-8',
        ):
        '''
        opts MUST contain 'fields', a list of field names.
        opts may also include 'headers', a list of field headings.
        opts MAY override any of the above configurables.
        '''
        self.fields = fields
        self.headers = headers or fields
        self.SEP = SEP
        self.QUOTE = QUOTE
        self.ESCQUOTE = ESCQUOTE or QUOTE + QUOTE
        self.LINEBREAK = LINEBREAK
        self.ENCODING = ENCODING

        def escape_field(val, SEP=self.SEP, QUOTE=self.QUOTE, ESCQ=self.ESCQUOTE):
            '''
            Escape separator and quote values, and wrap with quotes if needed

            Inlined for speed
            '''
            # escape quotes in the value
            val = val.replace(QUOTE, ESCQ)
            # if needed, wrap quotes around value
            if SEP in val or QUOTE in val:
                return QUOTE + val + QUOTE
            return val
        self.escape_field = escape_field

    def write(self, values):
        '''Write a row of values'''
        line = self.SEP.join(map(self.escape_field, values)) + self.LINEBREAK
        if self.ENCODING:
            line = line.encode(self.ENCODING)
        return line

    def write_dict(self, values):
        '''Write a row, getting values from a dict.'''
        return self.write(map(values.get, self.fields))

    def write_headers(self):
        '''Write a row of headers.'''
        return self.write(self.headers)
