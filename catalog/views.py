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

def signup(request):
    template = loader.get_template('catalog/signup.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'catalog/index.html'
#
#     # display blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     # process from data
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#             user = form.save(commit=False)
#
#             # cleaned (normalized) data
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.username = username
#             user.set_password(password)
#             user.save()