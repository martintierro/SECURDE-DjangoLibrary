from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *
from .forms import *

# Create your views here.

def index(request):
    template = loader.get_template('catalog/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

class UserFormView(View):
    form_class = UserForm
    template_name = 'catalog/signup.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process from data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            ID_number = form.cleaned_data['ID_number']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user.ID_number = ID_number
            user.username = username
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("index")

        return render(request, self.template_name, {'form': form})
