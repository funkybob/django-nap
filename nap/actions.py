
from django.http import StreamingHttpResponse
from django.utils.encoding import force_text

from .models import modelserialiser_factory

class CSV(object):
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


class ExportCsv(object):
    def __init__(self, serialiser=None, label=None, **opts):
        self.serialiser = serialiser
        self.opts = opts
        if label:
            self.short_description = label

    def __call__(self, admin, request, queryset):
        if self.serialiser is None:
            ser_class = modelserialiser_factory(
                '%sSerialiser' % admin.__class__.__name__,
                admin.model,
                **self.opts
            )
        else:
            ser_class = self.serialiser

        def inner(ser):
            csv = CSV(fields=ser._fields.keys())
            yield csv.write_headers()
            for obj in queryset:
                data = { 
                    key: force_text(val)
                    for key, val in ser.object_deflate(obj).items()
                }
                yield csv.write_dict(data)

        response = StreamingHttpResponse(inner(ser_class()), content_type='text/csv')
        filename = admin.csv_
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
