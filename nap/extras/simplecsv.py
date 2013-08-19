
import re

try:
    import chardet
except ImportError:
    chardet = None

class Writer(object):
    '''
    A generator friendly, unicode aware CSV encoder class built for speed.
    '''

    # What to put between fields
    SEP = u','
    # What to wrap fields in, if they contain SEP
    QUOTE = u'"'
    # What to replace a QUOTE in a field with
    ESCQUOTE = QUOTE + QUOTE
    # What to put between records
    LINEBREAK = u'\n'
    ENCODING = 'utf-8'

    fields = []

    def __init__(self, **opts):
        '''
        opts MUST contain 'fields', a list of field names.
        opts may also include 'headers', a list of field headings.
        opts MAY override any of the above configurables.
        '''
        self.__dict__.update(opts)

    def write(self, values):
        '''Write a row of values'''
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

        line = self.SEP.join(map(escape_field, values)) + self.LINEBREAK
        if self.ENCODING:
            line = line.encode(self.ENCODING)
        return line

    def write_dict(self, values):
        '''Write a row, getting values from a dict.'''
        return self.write(map(values.get, self.fields))

    def write_headers(self):
        '''Write a row of headers.'''
        return self.write(self.headers or self.fields)

class Reader(object):

    # What to put between fields
    SEP = u','
    # What to wrap fields in, if they contain SEP
    QUOTE = u'"'
    # What to replace a QUOTE in a field with
    ESCQUOTE = QUOTE + QUOTE
    # What to put between records
    LINEBREAK = u'\n'
    ENCODING = 'utf-8'

    def __init__(self, source, **opts):
        self.source = iter(source)
        self.__dict__.update(opts)
        self.field = re.compile(r'^(?P<quote>%(QUOTE)s?)([^%(SEP)s]+)(?P=quote)%(SEP)s?' % {
            'QUOTE': self.QUOTE,
            'SEP': self.SEP,
            'ESCQ': self.ESCQUOTE,
        })
        if self.ENCODING == 'auto' and chardet is None:
            raise ImportError('Encoding auto-detect requires chardet installed.')

    def __iter__(self):
        return self

    def next(self):
        line = self.source.next()
        if self.ENCODING == 'auto':
            line = line.decode(chardet.detect(line)['encoding'] or 'ascii')
        else:
            line = line.decode(self.ENCODING)

        fields = [ field.replace(self.ESCQUOTE, self.QUOTE) for quote, field in self.field.findall(line.strip())]
        return fields
