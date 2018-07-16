import logging
from functools import reduce

from django.db.models import Q
from django.db.models.fields.related import RelatedField
from pip._vendor.pyparsing import Each

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
    if 'pk' in queries.keys():
        q.append(Q(pk=queries.pop('pk')[0]))
    for query_key, query_value in queries.items():
        if query_key in valid_queries:
            query_value = query_value[0]
            has_attribute_field_and_is_related_field = hasattr(getattr(queryset.model, query_key), 'field') and isinstance(getattr(queryset.model, query_key).field, RelatedField)
            if has_attribute_field_and_is_related_field:
                q.append(Q(**{query_key: query_value}))
            else:
                q.append(Q(**{query_key + '__icontains': query_value}))
    if q:
        queryset = queryset.filter(
            reduce(lambda x, y: x & y, q)
        )
    return queryset
