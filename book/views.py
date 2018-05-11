from django.db.models import QuerySet, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from book.models import Book
from book.serializers import BookSerializer


def filter_book_list(queryset: QuerySet, **kwargs) -> QuerySet:
    if not kwargs:
        return queryset
    valid_queries = ['author', 'title']
    q = Q()
    for k,v in kwargs.items():
        if k in valid_queries:
            q = q & Q(**{k+'__icontains':v[0]})
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