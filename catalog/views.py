from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import *

# Create your views here.

def index(request):
    return HttpResponse('<h1>This is the catalog homepage</h1>')