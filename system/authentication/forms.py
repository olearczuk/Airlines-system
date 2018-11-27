from django import forms
from django.contrib.auth.models import User
from django.forms import Form, ValidationError, CharField


class RegistrationForm(Form):
    username = forms.CharField(max_length=50, label='username')
    password = forms.CharField(max_length=50, label='password', widget=forms.PasswordInput)

    def clean(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise ValidationError('User with this username exists.')


class LoginForm(Form):
    username = CharField(max_length=50, label='username')
    password = CharField(max_length=50, widget=forms.PasswordInput, label='password')
