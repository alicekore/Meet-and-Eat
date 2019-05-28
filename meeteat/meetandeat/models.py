from django.contrib.auth.models import AbstractUser
from django.core.validators import *
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse




# Create your models here.

class Event(models.Model):
    super_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=160)
    location = models.CharField(max_length=30)
    datetime = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)
    participants_number = models.IntegerField(default=2, validators=[MaxValueValidator(16), MinValueValidator(2)])

    def get_absolute_url(self):
        return reverse('meetandeat:event-view', args=[str(self.pk)])


class User(AbstractUser):
    profilePicture = models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True)
    visible = models.BooleanField(default=True)
