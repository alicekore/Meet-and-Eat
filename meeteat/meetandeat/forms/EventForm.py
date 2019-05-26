from django import forms


class EventForm(forms.Form):
    event_name = forms.CharField(label='eventName', max_length=50)
    description = forms.CharField(label='eventDescription', max_length=50, required=False)
    place = forms.CharField(label='eventPlace', max_length=50, required=False)
    person_number = forms.IntegerField(label="personNumber", min_value=2)
    datetime = forms.DateTimeField(label="datetime")

