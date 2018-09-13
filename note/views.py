from rest_framework.viewsets import ModelViewSet

from note.models import Note
from note.serializers import NoteSerializer


class NoteModelViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
