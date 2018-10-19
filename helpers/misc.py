import logging

from django.http import HttpResponse

logger = logging.getLogger(__name__)


def export_csv(queryset, *columns, **kwargs):
    lines = ''
    for c in columns[:-1]:
        lines += c
        lines += ', '
    lines += columns[-1:][0]
    for data in queryset:
        lines += '\n'
        for c in columns:
            try:
                _d = getattr(data, c)
                if isinstance(_d, dict):
                    _d = '"' + _d.__str__() + '"'
                lines += str(_d)
                if not c == columns[-1:][0]:
                    lines += ', '
            except Exception as e:
                logger.warning(e)

    response = HttpResponse(lines, content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    return response
