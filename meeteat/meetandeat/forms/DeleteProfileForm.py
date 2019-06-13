from django import forms
from meetandeat.models import User


class DeleteProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['password', ]
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'deleteAccountPassword',
                'required': True
            }),
        }