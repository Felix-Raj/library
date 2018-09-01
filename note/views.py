from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView

from note.models import Note
from note.serializers import NoteSerializer


class NoteListAPI(ListAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


class NoteCreateAPI(CreateAPIView):
    serializer_class = NoteSerializer

class NoteDeleteAPI(DestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
