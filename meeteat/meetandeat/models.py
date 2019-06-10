from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=160)
    location = models.CharField(max_length=30)
    datetime = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)
    reported = models.BooleanField(default=False)
    participants_number = models.IntegerField(default=2, validators=[MaxValueValidator(16), MinValueValidator(2)])
    tags = models.ManyToManyField(to='meetandeat.Tag')

    class Meta:
        permissions = [("join_event", 'Can join event'), ("hide_event", 'Can hide event'),
                       ('edit_event', 'Can Edit Event'), ('seeHidden_event', 'Can see hidden events')]

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        self.eventParticipants.add(self.user)

    def get_absolute_url(self):
        return reverse('meetandeat:event-view', args=[str(self.pk)])

    def __str__(self):
        return self.title


class Tag(models.Model):
    alphabetic = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters are allowed.')
    title = models.CharField(max_length=15, validators=[alphabetic])
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True

    def disapprove(self):
        self.approved = False

    def __str__(self):
        return self.title


class User(AbstractUser):
    profilePicture = models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True)
    visible = models.BooleanField(default=True)
    events = models.ManyToManyField(Event, related_name='eventParticipants', blank=True)
    reportedEvents = models.ManyToManyField(Event, related_name='userReportings', blank=True)
