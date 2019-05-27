from django import forms
from meetandeat.models import Event


class EventForm(forms.ModelForm):
    datetime = forms.DateTimeField(label="datetime", input_formats=['%Y-%m-%dT%H:%M'])

    class Meta:
        model = Event
        fields = ['title',
                  'description',
                  'location',
                  'participants_number',
                  'datetime']