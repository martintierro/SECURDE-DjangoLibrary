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
    template = loader.get_template('manager/books.html')
    books = Book.objects.all()
    count_dictionary = dict()
    for b in books:
        count = BookInstance.objects.filter(book=b).count()
        count_dictionary[b] = count
    context = {
        'count_dictionary': count_dictionary,
    }
    return HttpResponse(template.render(context, request))

def book_instances(request):
    template = loader.get_template('manager/book_instances.html')
    instances = BookInstance.objects.all()
    context = {
        'instances': instances,
    }
    return HttpResponse(template.render(context, request))

def add_book(request):
    template = loader.get_template('manager/add_book.html')
    authors = Author.objects.all()
    publishers = Publisher.objects.all()
    context = {
        'authors': authors,
        'publishers': publishers,
    }
    return HttpResponse(template.render(context, request))

def add_book_instance(request):
    template = loader.get_template('manager/add_book_instance.html')
    books = Book.objects.all()
    context = {
        'books': books,
    }
    return HttpResponse(template.render(context, request))

def change_password(request):
    template = loader.get_template('manager/change_password.html')
    context = {
    }
    return HttpResponse(template.render(context, request))