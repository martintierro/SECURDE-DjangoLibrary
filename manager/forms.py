from django.contrib.auth.models import User
from catalog.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
import re 
from django.db.models import Q

class ResetPasswordForm(UserCreationForm):
    current_password_flag = True #Used to raise the validation error when it is set to False
    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Current Password',}), label = "Current Password")
    # new_password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': 'New Password',}), label = "New Password")
    # confirm_new_password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Confirm New Password',}), label = "Confirm New Password")

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

class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title'}))
    year = forms.CharField(max_length=4, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Year of Publication'}))
    isbn = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '13 Character ISBN Number'}))
    
    class Meta:
        model = Book
        fields = ['title', 'year', 'isbn']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 2:
            raise ValidationError("Book Title is too short")
        if len(title) > 200:
            raise ValidationError("Book Title is too long")
        return title
    
    def clean_year(self):
        year = self.cleaned_data['year']
        if year.isdigit() is False:
            raise ValidationError("Year must only contain numbers")
        if len(year) > 4:
            raise ValidationError("Invalid year")
        return year

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']
        if isbn.isdigit() is False:
            raise ValidationError("ISBN must only contain numbers")
        if len(isbn) != 13:
            raise ValidationError("ISBN should be 13 digits")
        return isbn


class AuthorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=False)

    class Meta:
        model = Author
        fields = ['first_name', 'last_name']
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 2 and len(first_name) > 0:
            raise ValidationError("Author First Name is too short")
        if len(first_name) > 30:
            raise ValidationError("Author First Name is too long")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 2 and len(last_name) > 0:
            raise ValidationError("Author Last Name is too short")
        if len(last_name) > 30:
            raise ValidationError("Author Last Name is too long")
        return last_name
    
    def clean(self):
        cleaned_data = super(AuthorForm, self).clean()
        
        if (cleaned_data.get('first_name') == '' and cleaned_data.get('last_name') == '') or (cleaned_data.get('first_name') == '' and cleaned_data.get('last_name') == ''):
            raise ValidationError('Please fill out the empty author field')
        if (cleaned_data.get('first_name') == '' and cleaned_data.get('last_name') != '') or (cleaned_data.get('first_name') != '' and cleaned_data.get('last_name') == ''):
            raise ValidationError('Please fill out the empty author field')
        
        criterion1 = Q(first_name=cleaned_data.get('first_name'))
        criterion2 = Q(last_name=cleaned_data.get('last_name'))

        if Author.objects.filter(criterion1 & criterion2).exists():
            raise ValidationError("Author already exists")


class PublisherForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Publisher'}), required=False)

    class Meta:
        model = Publisher
        fields = ['name']
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) == 0:
            raise ValidationError("Input Publisher")
        if len(name) < 2:
            raise ValidationError("Publisher Name is too short")
        if len(name) > 200:
            raise ValidationError("Publisher Name is too long")
        if Publisher.objects.filter(name=name).exists():
            raise ValidationError("Publisher already exists")

        return name

STATUS = [
    ('a', 'Available'),
    ('r', 'Reserved'),
]

class BookInstanceForm(forms.ModelForm):
    status = forms.CharField(widget=forms.Select(attrs={'class': 'form-control custom-select h-100'}, choices=STATUS))
    class Meta:
        model = BookInstance
        fields = ['status']