from django import forms
from meetandeat.models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(label = "text",widget = forms.TextInput(attrs = {'class':"form-control",'placeholder':'Leave your comment here'}), max_length = 160)

    class Meta:
        model = Comment
        fields = ['text',]
