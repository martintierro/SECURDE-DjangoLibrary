from django.template import loader
from django.template.response import TemplateResponse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from catalog.models import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.admin.models import LogEntry
from .forms import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from axes.models import *
from itertools import chain

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
    if request.method == 'POST':
        user_form = ManagerUserForm(request.POST)
        profile_form = ManagerProfileForm(request.POST)
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
            user_group = Group.objects.get(name='Managers')
            user_group.user_set.add(user)
            user_group.save()
            current_user = User.objects.get(id=user.id)
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(User).pk,
                object_id=current_user.id,
                object_repr=current_user.username,
                action_flag=ADDITION)
            return redirect("view_managers")
        
    else:
        user_form = ManagerUserForm()
        profile_form = ManagerProfileForm()

    context = {
        'manager_user_form': user_form,
        'manager_profile_form': profile_form,
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
def access_logs(request):
    template = loader.get_template('catalog_admin/access_logs.html')
    log = AccessLog.objects.all()
    context = {
        'logs': log,
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('login'))
def access_attempts(request):
    template = loader.get_template('catalog_admin/access_attempts.html')
    log = AccessAttempt.objects.all()
    context = {
        'logs': log,
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('login'))
def change_password(request):
    template = loader.get_template('catalog_admin/change_password.html')
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
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ContentType.objects.get_for_model(User).pk,
                    object_id=user.id,
                    object_repr=user.username,
                    action_flag=CHANGE,
                    change_message="Changed password")
                login_user = authenticate(request=request, username=user.username, password=new_password)
                if user is not None:
                    if user.is_active:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        return redirect('admin_index')
            else:
                form.add_error('current_password', "Password is incorrect")

    else:
        form = ResetPasswordForm()
    context = {
        'reset_password_form': form,
    }
    return HttpResponse(template.render(context, request))