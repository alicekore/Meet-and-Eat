from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta


# Create your models here.

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=160)
    location = models.CharField(max_length=30)
    datetime = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)
    participants_number = models.IntegerField(default=2, validators=[MaxValueValidator(16), MinValueValidator(2)])
    tags = models.ManyToManyField(to='meetandeat.Tag')
    matching = models.IntegerField(default=101)

    class Meta:
        permissions = [("join_event", 'Can join event'), ("hide_event", 'Can hide event'),
                       ('edit_event', 'Can Edit Event'), ('seeHidden_event', 'Can see hidden events')]

        ordering = ('datetime',)

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        self.eventParticipants.add(self.user)

    def get_absolute_url(self):
        return reverse('meetandeat:event-view', args=[str(self.pk)])

    def hide_by_enough_reports(self):
        reportNumber = self.reports.filter(valid=None).count()
        if reportNumber >= 5:
            self.visible = False
            self.save()

    def leave(self, user):
        if user in self.eventParticipants.all():
            self.eventParticipants.remove(user)
            self.save()
    def set_matching(self, matching):
        self.matching = round(matching, 1)
        self.save()


class Tag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    alphabetic = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters are allowed.')

    title = models.CharField(max_length=15, validators=[alphabetic])
    description = models.CharField(max_length=160)
    disapprovalMsg = models.CharField(max_length=160)
    approved = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)

    def approve(self):
        self.approved = True

    def disapprove(self):
        self.approved = False

    def __str__(self):
        return self.title


class Report(models.Model):
    reportReason = models.TextField(blank=True, null=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reports')
    valid = models.BooleanField(null=True, blank=True, default=None)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=160)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class User(AbstractUser):
    # TODO: create a function to name files unique
    def user_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(self.id, filename)

    profilePicture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    visible = models.BooleanField(default=True)
    events = models.ManyToManyField(Event, related_name='eventParticipants', blank=True)
    ##reports = models.ManyToManyField(Report, related_name='users', blank=True)
    ##reportedEvents = models.ManyToManyField(Event, related_name='userReportings', blank=True)
    last_activation_attempt = models.DateTimeField(null=True, blank=True)
    activation_attempts_number = models.IntegerField(default=0)
    old_email = models.EmailField('old email address', null=True, blank=True)
    is_email_confirmed = models.BooleanField(default=False)

    def confirm_email(self):
        self.is_active = True
        self.activation_attempts_number = 0
        self.old_email = None
        self.is_email_confirmed = True
        self.last_activation_attempt = timezone.now() - timedelta(hours=1)

    def new_activation_attempt(self):
        self.last_activation_attempt = timezone.now()
        self.activation_attempts_number += 1

    def new_email(self):
        self.old_email = self.email
        self.is_email_confirmed = False

    def set_old_email(self):
        self.email = self.old_email
        self.is_email_confirmed = True

    def activation_attempt_failed(self):
        self.activation_attempts_number -= 1
        self.last_activation_attempt = timezone.now() - timedelta(hours=1)
