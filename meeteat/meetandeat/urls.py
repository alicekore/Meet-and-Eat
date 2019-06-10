from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

app_name = 'meetandeat'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-view'),
    path('event/<int:pk>/join', EventJoinView.as_view(), name='join-event'),
    path('event/create/', EventCreate.as_view(), name='create-event'),
    path('event/<int:pk>/edit/', EventUpdate.as_view(), name='edit-event'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', views.register, name='register'),
    path('mod/', modView.as_view(), name='modView'),
    path('mod/hide/<int:pk>/', modHide.as_view(), name='modHide'),
    path('mod/unhide/<int:pk>/', modUnhide.as_view(), name='modUnhide'),
    path('mod/unreport/<int:pk>/', modUnreport.as_view(), name='modUnreport'),
    path('tag/create/', TagCreate.as_view(), name='create-tag'),
    path('tag/<int:pk>/', TagDetailView.as_view(), name='tag-view'),
    path('tag/<int:pk>/edit/', TagUpdate.as_view(), name='edit-tag'),
    path('tag/all/', TagView.as_view(), name='tag-view'),


]
