from django.contrib.auth.models import User
from django import forms


class SignupForm(forms.ModelForm):
    ID_number = forms.CharField(max_length=8)
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['ID_number','username', 'password', 'first_name', 'last_name', 'email']

class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']
