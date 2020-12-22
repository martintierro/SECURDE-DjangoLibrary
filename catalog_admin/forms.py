from django.contrib.auth.models import User
from catalog.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _


class ManagerUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}), label="Username")
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}), label="First Name")
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}), label="Last Name")
    email = forms.EmailField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}), label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super(ManagerUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data    

class ManagerProfileForm (forms.ModelForm):
    # id_number = forms.IntegerField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'ID', 'style': "-webkit-appearance: none; margin: 0;"}), label="ID Number")
    id_number = forms.CharField(max_length=8, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ID', 'style': "-webkit-appearance: none; margin: 0;"}), label="ID Number")

    class Meta:
        model = Profile
        fields = ['id_number']


class ResetPasswordForm(forms.ModelForm):

    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Current Password',}), label = "Current Password")
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New Password',}), label = "New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm New Password',}), label = "Confirm New Password")

    class Meta:
        model = User
        fields = ['current_password', 'new_password', 'confirm_new_password']
    
    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password != confirm_new_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data