from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

app_name = 'meetandeat'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-view'),
    path('event/<int:pk>/join', EventJoinView.as_view(), name='join-event'),
    path('event/<int:pk>/leave', EventLeave.as_view(), name='leave-event'),
    path('event/<int:pk>/report', EventReport.as_view(), name='report-event'),
    path('event/create/', EventCreate.as_view(), name='create-event'),
    path('event/<int:pk>/edit/', EventUpdate.as_view(), name='edit-event'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my_events/', OwnEventsView.as_view(), name='own_events_list'),
    path('profile/edit', UserUpdateView.as_view(), name='edit-profile'),
    path('profile/delete-ajax', UserDeleteAjax.as_view(), name='delete-profile-ajax'),
    path('profile/delete', UserDeleteView.as_view(), name='delete-profile'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('activate_account/<str:uidb64>/<str:token>', UserActivateAccountView.as_view(), name='activate-account'),
    path('request_activation', RequestActivateAccountView.as_view(), name='request-activation'),
    path('request_email_confirm', RequestEmailConfirmView.as_view(), name='request-email-confirm'),
    path('password_reset/request', RequestPasswordResetView.as_view(), name='password-reset-request'),
    path('password_reset/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('mod/dashboard', ModView.as_view(), name='modView'),
    path('mod/hide/<int:pk>/', ModHide.as_view(), name='modHide'),
    path('mod/unreport/<int:pk>/', ModUnReport.as_view(), name='modUnreport'),
    path('tag/create/', TagCreate.as_view(), name='create-tag'),
    path('mod/tag/<int:pk>/', TagDetailView.as_view(), name='tag-details'),
    path('mod/tag/<int:pk>/edit/', TagUpdate.as_view(), name='edit-tag'),
    path('mod/tag/<int:pk>/approve/', ApproveTag.as_view(), name='approve-tag'),
    path('mod/tag/all/', TagView.as_view(), name='tag-view'),
    path('notifications/', NotificationView.as_view(), name='NotificationView'),

]
