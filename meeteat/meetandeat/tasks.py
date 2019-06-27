from django.utils import timezone
from .models import Event

def deleteEventsOlderThan(days):
    events = Event.objects.all()
    for e in events:
        diff = timezone.now() - e.datetime
        if diff.days >= days:
            e.delete()

def makeEventsInvisibleOlderThan(days):
    events = Event.objects.all()
    for e in events:
        diff = timezone.now() - e.datetime
        if diff.days >= days:
            e.visible = False
            e.save()