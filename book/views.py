import logging
from functools import reduce

from django.db.models import QuerySet, Q
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, get_object_or_404, UpdateAPIView, \
    DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import BookSerializer
from helpers.misc import export_csv

logger = logging.getLogger(__name__)
logger.warning(logger.name)  # use this name to configure loggers in LOGGING
logger.debug("This is a sample debug message")


def filter_book_list(queryset: QuerySet, **kwargs) -> QuerySet:
    logger.info('views.py:filter_book_list    kwargs {}'.format(kwargs))
    if not kwargs:
        return queryset
    valid_queries = ['author', 'title', 'booktag__tag', 'book_id', 'category']
    q = list()
    for k, v in kwargs.items():
        if k in valid_queries:
            q.append(Q(**{k + '__icontains': v[0]}))
    logger.debug(q)
    if q:
        queryset = queryset.filter(
            reduce(lambda x, y: x & y, q)
        )
    return queryset

# todo 9/13/18 felixraj : user viewset an in notes


class BookListView(ListAPIView):
    serializer_class = BookSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('author', 'title', 'booktag__tag', 'book_id', 'category')
    ordering_fields = ('author', 'title', 'book_id', 'category')

    def get_queryset(self):
        logger.info('views.py:get_queryset    kwargs {}'.format(self.request.query_params))
        queryset = Book.objects.all()
        queryset = filter_book_list(queryset, **self.request.query_params)
        return queryset


class BookDetailView(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class BookCreateView(CreateAPIView):
    serializer_class = BookSerializer


class BookEditView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDeleteView(DestroyAPIView):
    pass


class BookAddTagView(APIView):
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book.objects.all(), pk=kwargs.get('pk'))
        book.add_tag(request.GET.get('tags').split(','))
        return Response(data=BookSerializer(instance=book).data)


class LockBook(APIView):
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book.objects.all(), pk=kwargs.get('pk'))
        book.lock()
        return Response(data=self.serializer_class(instance=book).data)


class UnLockBook(APIView):
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        # TODO: change this to put
        book = get_object_or_404(Book.objects.all(), pk=kwargs.get('pk'))
        book.unlock()
        return Response(data=self.serializer_class(instance=book).data)


def export_book(request, *args, **kwargs):
    return export_csv(Book.objects.all(), 'pk', 'book_id', 'title', 'author', 'copies', 'notes', 'category', 'price', 'locked', 'preview')