from django.apps import AppConfig
from django.utils import timezone


class MeetandeatConfig(AppConfig):
    name = 'meetandeat'

    def ready(self):
        from .updater import start
        startdate = timezone.now() + timezone.timedelta(minutes=1)
        start(startdate)
