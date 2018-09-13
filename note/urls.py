from rest_framework.routers import DefaultRouter

from note.views import NoteModelViewSet

app_name = 'note'


router = DefaultRouter()
router.register('note', NoteModelViewSet, base_name='note')
urlpatterns = router.urls
