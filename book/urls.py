from django.urls import path

from book.views import BookListView, BookDetailView

app_name = 'book'
urlpatterns = [
    path('',BookListView.as_view(), name='book_list_api'),
    path('<int:pk>',BookDetailView.as_view(), name='book_detail_api'),
]