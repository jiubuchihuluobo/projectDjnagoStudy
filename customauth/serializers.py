from django import forms
from django.contrib.auth.forms import UserCreationForm

from customauth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MyRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=256)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
