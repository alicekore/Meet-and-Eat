from django import forms
from meetandeat.models import Tag


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title']