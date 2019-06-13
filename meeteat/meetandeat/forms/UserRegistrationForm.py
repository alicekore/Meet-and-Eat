from django.contrib.auth import *
from django.contrib.auth.forms import UserCreationForm



class UserRegistrationForm(UserCreationForm):

    class Meta:

        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name','profilePicture']


