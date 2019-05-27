from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.forms.widgets import DateTimeInput


class EventForm(forms.Form):
    title = forms.CharField(label='eventTitle', max_length=40)
    description = forms.CharField(label='eventDescription', max_length=160, required=False)
    location = forms.CharField(label='eventLocation', max_length=30, required=False)
    datetime = forms.DateTimeField(label="datetime", input_formats=['%Y-%m-%dT%H:%M'])
    participants_number = forms.IntegerField(label="personNumber", min_value=2, max_value=16)
