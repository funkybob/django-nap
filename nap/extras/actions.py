
from django.http import StreamingHttpResponse
from django.utils.encoding import force_text

from nap.serialiser.models import modelserialiser_factory

from .simplecsv import Writer


class ExportCsv(object):
    '''
    A factory class for Admin Actions to export a model as CSV.

    actions = [ ExportCsv(myserialiser, 'Export as CSV'), ]

    Optionally, you can pass kwargs to be passed to modelserialiser_factory to
    create a ModelSerialiser.
    '''
    def __init__(self, serialiser=None, label=None, **opts):
        self.serialiser = serialiser
        self.opts = opts
        if label:
            self.short_description = label
        self.__name__ = label or 'ExportCsv'

    def __call__(self, admin, request, queryset):
        if self.serialiser is None:
            ser_class = modelserialiser_factory(
                '%sSerialiser' % admin.__class__.__name__,
                admin.model,
                **self.opts
            )
        else:
            ser_class = self.serialiser

        select_related = self.opts.get('select_related', None)
        if select_related:
            queryset = queryset.select_related(*select_related)
        prefetch_related = self.opts.get('prefetch_related', None)
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)

        def inner(ser):
            csv = Writer(fields=self.opts.get('fields', ser._fields.keys()))
            yield csv.write_headers()
            for obj in queryset:
                data = {
                    key: force_text(val)
                    for key, val in ser.object_deflate(obj).items()
                }
                yield csv.write_dict(data)

        response = StreamingHttpResponse(inner(ser_class()), content_type='text/csv')
        filename = self.opts.get('filename', 'export_{classname}.csv')
        if callable(filename):
            filename = filename(admin)
        else:
            filename = filename.format(
                classname=admin.__class__.__name__,
                model=admin.model._meta.module_name,
                app_label=admin.model._meta.app_label,
            )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
