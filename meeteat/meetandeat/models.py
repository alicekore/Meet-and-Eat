from django.contrib.auth.models import AbstractUser
from django.core.validators import *
from django.db import models
from django.conf import settings

# Create your models here.

class Event(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=160)
    location = models.CharField(max_length=30)
    datetime = models.DateTimeField
    visible = models.BooleanField(default=True)
    participants = models.IntegerField(default=2, validators=[MaxValueValidator(16), MinValueValidator(2)])


class User(AbstractUser):
    profilePicture = models.ImageField(upload_to='photos/%Y/%m/%d')
    visible = models.BooleanField(default=True)
