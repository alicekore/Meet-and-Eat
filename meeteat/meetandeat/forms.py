from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput, TextInput
from django_select2.forms import Select2MultipleWidget

from meetandeat.models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='', widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='',
                               widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class RequestActivationLinkForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError({'username': ["This username does not exist", ]})
        if user.activation_attempts_number >= 3:
            raise ValidationError({'username': ["You have requested too many links", ]})
        if user.last_activation_attempt is not None \
                and user.last_activation_attempt + timedelta(hours=1) > timezone.now():
            raise ValidationError({'username': ["You have requested an activation link recently", ]})


class RequestPasswordResetLinkForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError({'username': ["This username does not exist", ]})


class ChangeProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profilePicture', ]

    def clean_profilePicture(self):
        profilePicture = self.cleaned_data.get("profilePicture")
        file_size = profilePicture.size
        limit_mb = 8
        if profilePicture is None:
            return profilePicture
        if file_size > limit_mb * 1024 * 1024:
            raise ValidationError("Max size of file is %s MB" % limit_mb)
        return profilePicture


class CommentForm(forms.ModelForm):
    text = forms.CharField(label="text",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Leave your comment here', 'autocomplete': 'off'}), max_length=160)

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
    tags_queryset = Tag.objects.filter(approved=True)
    tags = forms.ModelMultipleChoiceField(queryset=tags_queryset,
                                          widget=Select2MultipleWidget(attrs={'style': 'width: 100%;'}), required=False)

    date = forms.DateField(label="", input_formats=['%d/%m/%Y'])
    time = forms.TimeField(label="", input_formats=['%H:%M'])

    class Meta:
        model = Event
        fields = ['title',
                  'description',
                  'location',
                  'participants_number',
                  'date',
                  'time',
                  'tags']


class TagFilterForm(forms.Form):
    tags_queryset = Tag.objects.filter(approved=True)
    tags = forms.ModelMultipleChoiceField(required=False, queryset=tags_queryset,
                                          widget=Select2MultipleWidget(attrs={'style': 'width: 100%;', 'data-placeholder': 'Search by Tag', 'allowClear': True}))
    date = forms.DateField(widget=forms.DateInput(attrs={'autocomplete': 'off'}),
                           label="", input_formats=['%d/%m/%Y'], required=False)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'autocomplete': 'off'}),
                           label="", input_formats=['%H:%M'], required=False)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'title', 'description']

    def clean(self):
        title = self.cleaned_data.get('title')
        if Tag.objects.filter(title=title).exists():
            raise ValidationError("Tag already exists.")


class TagDisapprovalForm(forms.ModelForm):
    CHOICES = (
        ('Tag already exists.', 'Tag already exists.'),
        ('Tag is inappropriate.', 'Tag is inappropriate.'),
        ('Description not clear.', 'Description not clear.'),
    )
    disapprovalMsg = forms.CharField(widget=forms.Select(choices=CHOICES))

    class Meta:
        model = Tag
        fields = [
            'disapprovalMsg']


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # make user email field required
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'profilePicture']

    def clean_profilePicture(self):
        profilePicture = self.cleaned_data.get("profilePicture")
        if profilePicture is None:
            return profilePicture
        file_size = profilePicture.size
        limit_mb = 8
        if file_size > limit_mb * 1024 * 1024:
            raise ValidationError("Max size of file is %s MB" % limit_mb)
        return profilePicture
