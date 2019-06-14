from django import forms
from meetandeat.models import *
from django_select2.forms import Select2MultipleWidget
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class ChangeProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profilePicture', ]

    def clean_profilePicture(self):
        profilePicture = self.cleaned_data.get("profilePicture")
        file_size = profilePicture.size
        limit_mb = 8
        if file_size > limit_mb * 1024 * 1024:
            raise ValidationError("Max size of file is %s MB" % limit_mb)
        return profilePicture


class CommentForm(forms.ModelForm):
    text = forms.CharField(label="text", widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Leave your comment here'}), max_length=160)

    class Meta:
        model = Comment
        fields = ['text', ]


class DeleteProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password', ]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.instance.check_password(password):
            raise ValidationError("Entered password is not valid")
        return password


class EventForm(forms.ModelForm):
    datetime = forms.DateTimeField(label="datetime", input_formats=['%Y-%m-%dT%H:%M'])
    tags_queryset = Tag.objects.filter(approved=True)
    tags = forms.ModelMultipleChoiceField(queryset=tags_queryset,
                                          widget=Select2MultipleWidget(attrs={'style': 'width: 100%;'}),required=False)

    class Meta:
        model = Event
        fields = ['title',
                  'description',
                  'location',
                  'participants_number',
                  'datetime',
                  'tags']


class TagFilterForm(forms.Form):
    tags_queryset = Tag.objects.filter(approved=True)
    tags = forms.ModelMultipleChoiceField(required=False, queryset=tags_queryset, widget=Select2MultipleWidget(attrs={'style': 'width: 100%;', 'data-placeholder': 'Search by Tag', 'allowClear': True}))


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'title']


class UserRegistrationForm(UserCreationForm):

    class Meta:

        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'profilePicture']

    def clean_profilePicture(self):
        profilePicture = self.cleaned_data.get("profilePicture")
        file_size = profilePicture.size
        limit_mb = 8
        if file_size > limit_mb * 1024 * 1024:
            raise ValidationError("Max size of file is %s MB" % limit_mb)
        return profilePicture
