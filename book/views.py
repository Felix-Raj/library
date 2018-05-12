import logging

from django.db.models import QuerySet, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import BookSerializer

logger = logging.getLogger(__name__)
logger.warning(logger.name)  # use this name to configure loggers in LOGGING
logger.debug("This is a sample debug message")


def filter_book_list(queryset: QuerySet, **kwargs) -> QuerySet:
    if not kwargs:
        return queryset
    valid_queries = ['author', 'title']
    q = Q()
    for k, v in kwargs.items():
        if k in valid_queries:
            q = q & Q(**{k + '__icontains': v[0]})
    return queryset.filter(q)


class BookListView(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        queryset = filter_book_list(queryset, **self.request.GET)
        return queryset


class BookDetailView(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class BookCreateView(CreateAPIView):
    serializer_class = BookSerializer


class BookAddTagView(APIView):
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        logger.debug('request.GET')
        logger.debug(request.GET)
        book = get_object_or_404(Book.objects.all(), pk=kwargs.get('pk'))
        book.add_tag(request.GET.get('tags').split(','))
        return Response(data=BookSerializer(instance=book).data)
