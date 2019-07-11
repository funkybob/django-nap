
from django.http import StreamingHttpResponse

from .simplecsv import Writer


class ExportCsv:
    '''
    A factory class for Admin Actions to export a model as CSV.

    actions = [ ExportCsv(mymapper, 'Export as CSV'), ]

    '''
    def __init__(self, mapper=None, label=None, **opts):
        self.mapper = mapper
        self.opts = opts
        if label:
            self.short_description = label
        self.__name__ = label or 'ExportCsv'

    def __call__(self, admin, request, queryset):
        mapper = self.mapper()

        select_related = self.opts.get('select_related', None)
        if select_related:
            queryset = queryset.select_related(*select_related)
        prefetch_related = self.opts.get('prefetch_related', None)
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)

        def inner():
            csv = Writer(fields=self.opts.get('fields', mapper._fields.keys()))
            yield csv.write_headers()
            for obj in queryset:
                data = mapper << obj
                yield csv.write_dict(data)

        response = StreamingHttpResponse(inner(), content_type='text/csv')
        filename = self.opts.get('filename', 'export_{classname}.csv')
        if callable(filename):
            filename = filename(admin)
        else:
            filename = filename.format(
                classname=admin.__class__.__name__,
                model=admin.model._meta.model_name,
                app_label=admin.model._meta.app_label,
            )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
