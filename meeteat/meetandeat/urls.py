from django.urls import path

from .views import *

app_name = 'meetandeat'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('event/create', CreateEventView.as_view(), name='create-event'),
    path('event/<int:event_id>/edit', EditEventView.as_view(), name='edit-event'),
]
