from django.urls import path

from . import views

app_name = 'meetandeat'

urlpatterns = [
    path('', views.index, name='index'),
]