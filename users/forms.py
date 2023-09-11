from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import get_user_model
User = get_user_model()


class RegisterForm(UserCreationForm):
    # Form for handing user registration
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
