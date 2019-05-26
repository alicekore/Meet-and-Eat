from django import forms


class EventForm(forms.Form):
    event_name = forms.CharField(label='eventName', max_length=40)
    description = forms.CharField(label='eventDescription', max_length=160, required=False)
    place = forms.CharField(label='eventPlace', max_length=30, required=False)
    person_number = forms.IntegerField(label="personNumber", min_value=2, max_value=16)
    datetime = forms.DateTimeField(label="datetime")

