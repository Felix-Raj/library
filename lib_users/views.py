import logging
from datetime import timedelta, datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.six import BytesIO
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.filters import filter_qs
from helpers.misc import export_csv
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

    def perform_create(self, serializer):
        super(LibUsersCreateView, self).perform_create(serializer)


class AccountActivateDeactivateAPI(APIView):
    serializer_class = LibUsersSerializer

    def put(self, request, *args, **kwargs):
        user: LibUsers = get_object_or_404(LibUsers, pk=kwargs.get('pk'))
        if kwargs.get('state') == 'activate':
            user.activate_account()
        else:
            user.de_activate_account()
        return Response(data=self.serializer_class(user).data)


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
        # serializer.save(duration=serializer.validated_data.get('duration', timedelta(seconds=Lent.DEFAULT_LENT_DURATION))*24*60*60)
        duration: timedelta = serializer.validated_data.get('duration', timedelta(days=0))
        if duration.days == 0:
            if duration.seconds != 0:
                duration = timedelta(days=duration.seconds)
            elif duration.microseconds != 0:
                duration = timedelta(days=duration.microseconds)
        serializer.save(duration=duration)


class LentReceivedAPI(DestroyAPIView):
    queryset = Lent.objects.all()


class LentToUserAPI(APIView):
    def get(self, *args, **kwargs):
        # todo 7/28/18 felixraj : may apply pagination
        user = get_object_or_404(LibUsers, pk=self.kwargs.get('pk'))
        return Response(data=LentListSerializer(instance=user.lent_status(), many=True).data)


class LentDueAPI(APIView):
    model = Lent
    serializer = LentListSerializer

    def get_queryset(self):
        return self.model.objects.all().order_by('lent_on')

    def get(self, *args, **kwargs):
        today = datetime.today().date()
        target_date = today + timedelta(days=7)

        lents = list()
        for lent in self.get_queryset():
            if lent.due_on <= target_date:
                lents.append(lent)

        return Response(data=self.serializer(instance=lents, many=True).data)


class LentRenewAPI(APIView):
    model = Lent
    serializer_class = LentSerializer

    def put(self, *args, **kwargs):
        lent: Lent = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        period = self.request.data.get('period', timedelta(days=7))
        lent.renew_lent(period=period)
        return Response(data=self.serializer_class(instance=lent).data)


class BirthdayAlertAPI(APIView):
    def get(self, *args, **kwargs):
        # todo 7/28/18 felixraj : may apply pagination
        today = datetime.today().date()
        target_one = today + timedelta(days=0)
        target_end = today + timedelta(days=7)

        users = list()
        for user in LibUsers.objects.all().order_by('-date_of_birth'):
            user_next_birthday = datetime(year=today.year, month=user.date_of_birth.month, day=user.date_of_birth.day).date()
            if target_one <= user_next_birthday <= target_end:
                users.append(user)

        users.sort(key=lambda x: x.date_of_birth.month)

        return Response(data=LibUsersSerializer(instance=list(users), many=True).data)


def export_users(request, *args, **kwargs):
    return export_csv(LibUsers.objects.all(), 'id', 'name', 'uid', 'avatar', 'user_type', 'account_activated', 'date_of_birth','father', 'mother')