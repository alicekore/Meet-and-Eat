from django.utils import timezone
from .models import Event

def deleteEvents():
    # Events older than 'days' will be deleted
    days = 7

    events = Event.objects.all()
    for e in events:
        diff = timezone.now() - e.datetime
        if diff.days >= days:
            e.delete()
            
    print('Database updated: Deleted events older than 7 days.')

def makeEventsInvisible():
    # Events older than 'days' will be made invisible
    days = 1

    events = Event.objects.all()
    if events:
        for e in events:
            diff = timezone.now() - e.datetime
            if diff.days >= days:
                e.visible = False
                e.save()

    print('Database updated: Made events older than 1 day invisible.')
