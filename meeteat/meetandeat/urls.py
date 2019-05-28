from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

app_name = 'meetandeat'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-view'),
    path('event/create/', EventCreate.as_view(), name='create-event'),
    path('event/<int:pk>/edit/', EventUpdate.as_view(), name='edit-event'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile', ProfileView.as_view(), name='profile'),

]
