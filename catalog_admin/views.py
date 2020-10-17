from django.template import loader
from django.template.response import TemplateResponse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from catalog.models import *
from django.db.models import Q
# Create your views here.
def index(request):
    template = loader.get_template('catalog_admin/users.html')
    users = User.objects.filter(groups__name='Users')
    context = {
        'users' : users,
    }
    return HttpResponse(template.render(context, request))

def view_managers(request):
    template = loader.get_template('catalog_admin/managers.html')
    managers = User.objects.filter(groups__name='Managers')
    context = {
        'managers' : managers,
    }
    return HttpResponse(template.render(context, request))

def add_manager(request):
    template = loader.get_template('catalog_admin/add_manager.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def system_logs(request):
    template = loader.get_template('catalog_admin/system_logs.html')
    context = {
    }
    return HttpResponse(template.render(context, request))