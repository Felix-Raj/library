import logging

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView

from helpers.filters import filter_qs
from lib_users.models import Lent, LibUsers
from lib_users.serializers import LentSerializer, LibUsersSerializer, LentListSerializer

logger = logging.getLogger(__name__)


def filter_lent_list(queryset, **kwargs):
    # todo 5/23/18 felixraj : search by lent on date
    logger.info('Querying for '+kwargs.__str__())
    return filter_qs(queryset, ['lib_user', 'book', 'lib_user__name', 'book__title', 'pk'], **kwargs)


def filter_user_list(queryset, **kwargs):
    return filter_qs(queryset, ['name', 'uid', 'pk'], **kwargs)


class LibUserListView(ListAPIView):
    serializer_class = LibUsersSerializer

    def get_queryset(self):
        queryset = LibUsers.objects.all()
        return filter_user_list(queryset, **self.request.GET)


class LibUsersCreateView(CreateAPIView):
    serializer_class = LibUsersSerializer


class LentListView(ListAPIView):
    serializer_class = LentListSerializer

    def get_queryset(self):
        queryset = Lent.objects.all()
        return filter_lent_list(queryset, **self.request.GET)


class LentCreateAPI(CreateAPIView):
    serializer_class = LentSerializer

    # todo 5/23/18 felixraj : validate weather book is actually available for lent
    # http://www.django-rest-framework.org/api-guide/serializers/#validation

    def perform_create(self, serializer):
        serializer.save(duration=serializer.validated_data.get('duration')*24*60*60)
