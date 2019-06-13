from django import forms
from meetandeat.models import Tag, Event
from django_select2.forms import Select2MultipleWidget


class EventForm(forms.ModelForm):
    datetime = forms.DateTimeField(label="datetime", input_formats=['%Y-%m-%dT%H:%M'])
    tags_queryset = Tag.objects.filter(approved=True)
    tags = forms.ModelMultipleChoiceField(queryset=tags_queryset,
                                          widget=Select2MultipleWidget(attrs={'style': 'width: 100%;'}))

    class Meta:
        model = Event
        fields = ['title',
                  'description',
                  'location',
                  'participants_number',
                  'datetime',
                  'tags']
