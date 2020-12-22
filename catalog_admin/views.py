from django.template import loader
from django.template.response import TemplateResponse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from catalog.models import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.admin.models import LogEntry
from .forms import *

# Create your views here.
@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('login'))
def index(request):
    template = loader.get_template('catalog_admin/users.html')
    users = User.objects.filter(groups__name='Users')
    context = {
        'users' : users,
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('login'))
def view_managers(request):
    template = loader.get_template('catalog_admin/managers.html')
    managers = User.objects.filter(groups__name='Managers')
    context = {
        'managers' : managers,
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('login'))
def add_manager(request):
    template = loader.get_template('catalog_admin/add_manager.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('login'))
def system_logs(request):
    template = loader.get_template('catalog_admin/system_logs.html')
    logs = LogEntry.objects.all() #or you can filter, etc.
    context = {
        'logs': logs,
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('login'))
def change_password(request):
    template = loader.get_template('catalog_admin/change_password.html')
    print(request.method)
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']
            check_authentication = check_password(current_password, user.password)

            if check_authentication:
                user.set_password(new_password)   
                user.save()
                login_user = authenticate(username=user.username, password=new_password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('admin_index')
            else:
                form.add_error('current_password', "Password is incorrect")

    else:
        form = ResetPasswordForm()
    context = {
        'reset_password_form': form,
    }
    return HttpResponse(template.render(context, request))