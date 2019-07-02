from django.apps import AppConfig

class MeetandeatConfig(AppConfig):
    name = 'meetandeat'

    def ready(self):
        from .updater import start
        from .tasks import deleteEvents, makeEventsInvisible

        start()
