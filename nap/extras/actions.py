
from django.http import StreamingHttpResponse
from django.utils.encoding import force_text

from .models import modelserialiser_factory
from .simplecsv import CSV


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
