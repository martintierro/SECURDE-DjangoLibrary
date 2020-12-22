from django.contrib.auth.models import User
from catalog.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _


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