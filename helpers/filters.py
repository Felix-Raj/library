import logging
from functools import reduce

from django.db.models import Q
from django.db.models.fields.related import RelatedField

logger = logging.getLogger(__name__)


def filter_qs(queryset, valid_queries, **queries):
    """
    Filter the queryset.
    :param queryset: QuerySet to filter
    :param valid_queries: An Array of possible queries
    :param queries: queries to make
    :return: QuerySet which is filtered of queryset
    """
    # todo 5/31/18 felixraj : Change valid_queries from list to dict. dict having keys the name of the parameter that
    # ... appear in the URL, and value the actual field in which the search is to be performed
    if not queries:
        return queryset
    q = list()
    for k, v in queries.items():
        if k in valid_queries:
            v = v[0]
            if isinstance(getattr(queryset.model, k).field, RelatedField):
                q.append(Q(**{k: v}))
            else:
                q.append(Q(**{k + '__icontains': v}))
    if q:
        queryset = queryset.filter(
            reduce(lambda x, y: x & y, q)
        )
    return queryset
