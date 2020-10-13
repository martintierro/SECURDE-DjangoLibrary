from django.contrib.auth.models import User
from .models import Profile
from django import forms


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'USERNAME'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'FIRSTNAME'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'LASTNAME'}))
    email = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'EMAIL'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'PASSWORD'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'CONFIRM PASSWORD'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    # def clean(self):
    #     cleaned_data = super(UserForm, self).clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")

    #     if password != confirm_password:
    #         self.add_error('confirm_password', "Password does not match")

    #     return cleaned_data


class ProfileForm (forms.ModelForm):
    id_number = forms.CharField(max_length=8, widget=forms.TextInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'ID'}))

    class Meta:
        model = Profile
        fields = ['id_number']


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class EditPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'CONFIRM PASSWORD'}))

    class Meta:
        model = User
        fields = ['password']
