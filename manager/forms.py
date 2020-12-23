from django.contrib.auth.models import User
from catalog.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

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

class AddBookForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title'}))
    # author = forms.ForeignKey(widget=forms.TextInput(
    #     attrs={'class': 'form-control'}))
    # publisher = forms.ForeignKey(widget=forms.TextInput(
    #     attrs={'class': 'form-control'}))
    year = forms.CharField(max_length=4, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Year of Publication'}))
    isbn = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '13 Character ISBN Number'}))
    
    class Meta:
        model = Book
        fields = ['title', 'year', 'isbn']

class AddAuthorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=False)

    class Meta:
        model = Author
        fields = ['first_name', 'last_name']
    
    def clean(self):
        cleaned_data = super(AddAuthorForm, self).clean()
        if (cleaned_data.get('first_name') == '' and cleaned_data.get('last_name') != '') or (cleaned_data.get('first_name') != '' and cleaned_data.get('last_name') == ''):
            raise ValidationError('Please fill out the empty author field')


class AddPublisherForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Publisher'}), required=False)

    class Meta:
        model = Publisher
        fields = ['name']