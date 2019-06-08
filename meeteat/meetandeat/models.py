from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Group


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

    ##add transactional func.
    ##create Group with creation of Event
    def save(self,*args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        Group.objects.create(name=(self.title+'_'+str(self.pk)),event=self)

    def get_absolute_url(self):
        return reverse('meetandeat:event-view', args=[str(self.pk)])
    class Meta:
        permissions=[("join_event",'Can join event'),("hide_event",'Can hide event'),('edit_event','Can Edit Event'),('seeHidden_event','Can see hidden events')]


class User(AbstractUser):
    profilePicture = models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True)
    visible = models.BooleanField(default=True)

##Group for Users in Events
class Group(Group):
    event=models.OneToOneField(Event,on_delete=models.CASCADE,blank=True,related_name='groupEvent')
    users=models.ManyToManyField(settings.AUTH_USER_MODEL)



