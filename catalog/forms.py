from django.contrib.auth.models import User
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re 

class UserForm(UserCreationForm):
    # username = forms.CharField(max_length=50, widget=forms.TextInput(
    #     attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'USERNAME'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'FIRSTNAME'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'LASTNAME'}))
    email = forms.EmailField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'EMAIL'}))
    # password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'PASSWORD'}))
    # confirm_password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'CONFIRM PASSWORD'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-item mx-auto'
        self.fields['password1'].widget.attrs['class'] = 'form-control form-item mx-auto'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-item mx-auto'
        self.fields['username'].widget.attrs['placeholder'] = 'USERNAME'
        self.fields['password1'].widget.attrs['placeholder'] = 'PASSWORD'
        self.fields['password2'].widget.attrs['placeholder'] = 'CONFIRM PASSWORD'
    
    def clean_email(self):
        regex = '^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
        email = self.cleaned_data['email']
        if(not re.search(regex,email)): 
            raise ValidationError("Input a valid email address")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        if len(username) < 2:
            raise ValidationError("Username is too short")
        if len(username) > 30:
            raise ValidationError("Username is too long")
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 2:
            raise ValidationError("First Name is too short")
        if len(first_name) > 30:
            raise ValidationError("First Name is too long")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 2:
            raise ValidationError("Last Name is too short")
        if len(last_name) > 30:
            raise ValidationError("Last Name is too long")
        return last_name


class ProfileForm (forms.ModelForm):
    # id_number = forms.IntegerField(widget=forms.TextInput(
    #     attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'ID'}))
    id_number = forms.CharField(max_length=8, widget=forms.TextInput(
        attrs={'class': 'form-control form-item mx-auto', 'placeholder': 'ID'}))

    class Meta:
        model = Profile
        fields = ['id_number']

    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']
        if id_number.isdigit() is False:
            raise ValidationError("ID Number must only contain numbers")
        if len(id_number) != 8:
            raise ValidationError("ID Number should be 8 digits")
        return id_number



class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class ResetPasswordForm(UserCreationForm):
    current_password_flag = True #Used to raise the validation error when it is set to False
    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-change-item', 'placeholder': 'CURRENT PASSWORD'}))
    # new_password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control form-change-item', 'placeholder': 'NEW PASSWORD'}))
    # confirm_new_password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control form-change-item', 'placeholder': 'CONFIRM NEW PASSWORD'}))

    class Meta:
        model = User
        fields = ['current_password', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control form-change-item'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-change-item'
        self.fields['password1'].widget.attrs['placeholder'] = 'NEW PASSWORD'
        self.fields['password2'].widget.attrs['placeholder'] = 'CONFIRM NEW PASSWORD'
    
    def set_current_password_flag(self): 
        self.current_password_flag = False
        return 0

    def clean_current_password(self, *args, **kwargs):
        current_password = self.cleaned_data.get('current_password')

        if self.current_password_flag == False:
            raise ValidationError("Incorrect current password")

        return current_password


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