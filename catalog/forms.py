from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    ID_number = forms.CharField(max_length=8)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['ID_number', 'password']
