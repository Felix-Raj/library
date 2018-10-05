import logging

from django.http import HttpResponse

logger = logging.getLogger(__name__)


def export_csv(queryset, *columns, **kwargs):
    lines = ''
    for c in columns:
        lines += c
        lines += ', '
    for data in queryset:
        lines += '\n'
        for c in columns:
            try:
                _d = getattr(data, c)
                if isinstance(_d, dict):
                    _d = '"'+_d.__str__()+'"'
                lines += str(_d)
                lines += ', '
            except Exception as e:
                logger.warn(e)

    response = HttpResponse(lines, content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    return response