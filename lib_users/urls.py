from django.urls import path

from lib_users.views import LentListView, LentCreateAPI, LibUserListView, LibUsersCreateView, LentReceivedAPI

app_name = 'lib_users'
urlpatterns = [
    path('', LibUserListView.as_view(), name='lib_user_list'),
    path('new/', LibUsersCreateView.as_view(), name='lib_user_create'),
    path('lent/', LentListView.as_view(), name='lent_list'),
    path('lent/new/', LentCreateAPI.as_view(), name='lent_create'),
    path('lent/return/<int:pk>/', LentReceivedAPI.as_view(), name='lent_receive'),
]