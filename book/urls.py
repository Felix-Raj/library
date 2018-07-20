from django.urls import path

from book.views import (BookListView, BookDetailView, BookCreateView, BookAddTagView, LockBook)

app_name = 'book'
urlpatterns = [
    path('', BookListView.as_view(), name='book_list_api'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail_api'),
    path('new/', BookCreateView.as_view(), name='book_new'),
    path('<int:pk>/tag/', BookAddTagView.as_view(), name='book_add_tag_api'),
    path('<int:pk>/lock/', LockBook.as_view(), name='lock_book_api'),
    path('<int:pk>/unlock/', LockBook.as_view(), name='lock_book_api'),
]
