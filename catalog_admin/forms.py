from django.contrib.auth.models import User
from catalog.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re 

class ManagerUserForm(UserCreationForm):
    # username = forms.CharField(max_length=50, widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Username'}), label="Username")
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}), label="First Name")
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}), label="Last Name")
    email = forms.EmailField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}), label="Email Address")
    # password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Password'}), label="Password")
    # confirm_password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Password'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(ManagerUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def clean_email(self):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
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

class ManagerProfileForm (forms.ModelForm):
    # id_number = forms.IntegerField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'ID', 'style': "-webkit-appearance: none; margin: 0;"}), label="ID Number")
    id_number = forms.CharField(max_length=8, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ID', 'style': "-webkit-appearance: none; margin: 0;"}), label="ID Number")

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

class ResetPasswordForm(UserCreationForm):
    current_password_flag = True #Used to raise the validation error when it is set to False
    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Current Password',}), label = "Current Password")

    class Meta:
        model = User
        fields = ['current_password', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm New Password'
    
    def set_current_password_flag(self): 
        self.current_password_flag = False
        return 0

    def clean_current_password(self, *args, **kwargs):
        current_password = self.cleaned_data.get('current_password')

        if self.current_password_flag == False:
            raise ValidationError("Incorrect current password")

        return current_password