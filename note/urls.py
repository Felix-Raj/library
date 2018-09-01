from django.urls import path

from note.views import NoteListAPI, NoteCreateAPI, NoteDeleteAPI

app_name = 'note'
urlpatterns = [
    path('', NoteListAPI.as_view(), name='note_list'),
    path('new/', NoteCreateAPI.as_view(), name='note_create'),
    path('<int:pk>/delete/', NoteDeleteAPI.as_view(), name='note_delete'),
]
