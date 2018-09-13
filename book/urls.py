from django.urls import path

from book.views import (BookListView, BookDetailView, BookCreateView, BookAddTagView, LockBook, UnLockBook,
                        BookEditView)

app_name = 'book'
urlpatterns = [
    path('', BookListView.as_view(), name='book_list_api'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail_api'),
    path('new/', BookCreateView.as_view(), name='book_new'),
    path('<int:pk>/edit/', BookEditView.as_view(), name='book_edit_api'),
    path('<int:pk>/tag/', BookAddTagView.as_view(), name='book_add_tag_api'),
    path('<int:pk>/lock/', LockBook.as_view(), name='lock_book_api'),
    path('<int:pk>/unlock/', UnLockBook.as_view(), name='unlock_book_api'),
]
