from django.template import loader
from django.template.response import TemplateResponse
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *
from .forms import *

# Create your views here.

def index(request):
    template = loader.get_template('catalog/books.html')
    books = Book.objects.all()
    instances = BookInstance.objects.all()
    context = {
        'books': books,
        'instances': instances,
    }
    return HttpResponse(template.render(context, request))

class SignupView(View):
    user_form_class = UserForm
    profile_form_class = ProfileForm
    template_name = 'catalog/signup.html'

    # display blank form
    def get(self, request):
        user_form = self.user_form_class(None)
        profile_form = self.profile_form_class(None)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    # process from data
    def post(self, request):
        user_form = self.user_form_class(request.POST)
        profile_form =  self.profile_form_class(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)

            # cleaned (normalized) data
            id_number = profile_form.cleaned_data['id_number']
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            user.username = username
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            user.profile.id_number = id_number
            user.save()

            user = authenticate(username=username,password=password)

            

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("index")

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })
