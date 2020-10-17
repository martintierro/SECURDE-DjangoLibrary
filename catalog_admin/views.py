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
        'users':users,
    }
    return HttpResponse(template.render(context, request))

def view_managers(request):
    template = loader.get_template('catalog_admin/managers.html')
    managers = User.objects.filter(groups__name='Managers')
    context = {
        'managers': managers,
    }
    return HttpResponse(template.render(context, request))
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             books = Book.objects.filter(Q(title__icontains=query) | Q(author__in=Author.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))) )   
#         else:
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     else:
#         books = Book.objects.all()
#         form = SearchForm()
#     template = loader.get_template('')
#     instances = BookInstance.objects.all()
#     status_dictionary = dict()
#     for b in books:
#         status = 'r'
#         for i in instances:
#             if i.book.isbn == b.isbn:
#                 if i.status == 'a':
#                     status = 'a'
#         status_dictionary[b] = status

#     context = {
#         'books': books,
#         'instances': instances,
#         'status_dictionary': status_dictionary,
#         'search_form': form,
#     }
#     return HttpResponse(template.render(context, request))