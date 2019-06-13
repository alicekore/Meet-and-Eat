from django import forms
from meetandeat.models import User


class ChangeProfilePicture(forms.ModelForm):

    class Meta:
        model = User
        fields = ['profilePicture', ]