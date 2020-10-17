from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def check_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return HttpResponseRedirect(reverse('admin_index'))
        if request.user.groups.filter(name='Users').exists():
            return HttpResponseRedirect(reverse('catalog_index'))
        elif request.user.groups.filter(name='Users').exists():
            return HttpResponseRedirect(reverse('manager_index'))
        
    else:
        return HttpResponseRedirect(reverse('catalog_index'))

    context = {}
    template = "index.html"
    return render(request, template, context)
