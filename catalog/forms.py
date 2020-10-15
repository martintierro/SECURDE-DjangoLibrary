from django.contrib.auth.models import User
from .models import *
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

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data


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


class ResetPasswordForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-change-item', 'placeholder': 'CURRENT PASSWORD'}))
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-change-item', 'placeholder': 'NEW PASSWORD'}))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-change-item', 'placeholder': 'CONFIRM NEW PASSWORD'}))

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

class ReviewForm(forms.ModelForm):
    text = forms.CharField(max_length=1000, widget=forms.Textarea(
        attrs={'class': 'form-control w-100 review_input', 'placeholder': 'Enter text...', 'rows': '2'}), label='')
    
    class Meta:
        model = Review
        fields = ['text']

class SearchForm(forms.ModelForm):
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search'}), label='')

    class Meta:
        model = Book
        fields = ['query']