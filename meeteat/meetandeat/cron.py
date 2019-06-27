from django_cron import CronJobBase, Schedule
from .models import Event
from django.utils import timezone

"""
This file is not in use yet, but could be used for productions tasks.
"""

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 2  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'meetandeat.my_cron_job'    # a unique code

    def do(self):
        events = Event.objects.all()
        for e in events:
            diff = timezone.now() - e.datetime
            if diff.days >= 7:
                e.delete()
        print('Cleared old events')


def my_scheduled_job():
    events = Event.objects.all()
    for e in events:
        diff = timezone.now() - e.datetime
        if diff.days >= 7:
            e.delete()
    print('Cleared old events')
