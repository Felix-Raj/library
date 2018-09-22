from django.urls import path

from lib_users.views import (LentListView, LentCreateAPI, LibUserListView,
                             LibUsersCreateView, LentReceivedAPI,
                             BirthdayAlertAPI, LentToUserAPI, LentDueAPI,
                             AccountActivateDeactivateAPI)

app_name = 'lib_users'
urlpatterns = [
    path('', LibUserListView.as_view(), name='lib_user_list'),
    path('<int:pk>/activate/', AccountActivateDeactivateAPI.as_view(), name='lib_user_activate'),
    path('<int:pk>/deactivate/', AccountActivateDeactivateAPI.as_view(), name='lib_user_de_activate'),
    path('birthdays/', BirthdayAlertAPI.as_view(), name='lib_user_birthdays'),
    path('new/', LibUsersCreateView.as_view(), name='lib_user_create'),
    path('lent/', LentListView.as_view(), name='lent_list'),
    path('lent/new/', LentCreateAPI.as_view(), name='lent_create'),
    path('<int:pk>/lent/pending/', LentToUserAPI.as_view(), name='lent_to_user'),
    path('lent/return/<int:pk>/', LentReceivedAPI.as_view(), name='lent_receive'),
    path('lent/recent_dues/', LentDueAPI.as_view(), name='lent_recent_dues'),
]