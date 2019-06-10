from django import forms
from meetandeat.models import Tag
from django_select2.forms import Select2MultipleWidget


class TagFilterForm(forms.Form):
    tags_queryset = Tag.objects.filter(approved=True)
    tags = forms.ModelMultipleChoiceField(required=False, queryset=tags_queryset, widget=Select2MultipleWidget(attrs={'style': 'width: 100%;', 'data-placeholder': 'Search by Tag', 'allowClear': True}))

