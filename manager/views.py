from django.template import loader
from django.template.response import TemplateResponse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from catalog.models import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import user_passes_test
from .forms import *
# Create your views here.

@user_passes_test(lambda u: u.groups.filter(name='Managers').exists(), login_url=reverse_lazy('login'))
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

@user_passes_test(lambda u: u.groups.filter(name='Managers').exists(), login_url=reverse_lazy('login'))
def book_instances(request):
    template = loader.get_template('manager/book_instances.html')
    instances = BookInstance.objects.all()
    context = {
        'instances': instances,
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u: u.groups.filter(name='Managers').exists(), login_url=reverse_lazy('login'))
def add_book(request):
    template = loader.get_template('manager/add_book.html')
    authors = Author.objects.all()
    publishers = Publisher.objects.all()

    if request.method == 'POST':
        book_form = BookForm(data=request.POST)
        author_form = AuthorForm(data=request.POST)
        publisher_form = PublisherForm(data=request.POST)
        
        selected_author = None   
        selected_publisher = None   
        
        if book_form.is_valid():
            if request.POST.get('author_id') is not None:
                selected_author = get_object_or_404(Author, pk=request.POST.get('author_id'))
            elif author_form.is_valid() and author_form.has_changed():
                author = author_form.save(commit=False)
                first_name = author_form.cleaned_data['first_name']
                last_name = author_form.cleaned_data['last_name']
                author.first_name = first_name
                author.last_name = last_name
                author.save()
                selected_author = Author.objects.get(id=author.id)

           
            if request.POST.get('publisher_id') is not None:
                selected_publisher = get_object_or_404(Publisher, pk=request.POST.get('publisher_id'))
            elif publisher_form.is_valid() and publisher_form.has_changed():
                publisher_object = publisher_form.save(commit=False)
                publisher_name = publisher_form.cleaned_data['name']
                publisher_object.name = publisher_name
                publisher_object.save()
                selected_publisher = Publisher.objects.get(id=publisher_object.id)
            
            if book_form.is_valid() and selected_publisher is not None and selected_author is not None:
                book = book_form.save(commit=False)
                

                title = book_form.cleaned_data['title']
                year = book_form.cleaned_data['year']
                isbn = book_form.cleaned_data['isbn']
                
                book.title = title
                book.author = selected_author
                book.publisher = selected_publisher
                book.year = year
                book.isbn = isbn

                book.save()

                return redirect('manager_index')
        else:
            return redirect('add_book')

    else:
        book_form = BookForm()
        author_form = AuthorForm()
        publisher_form = PublisherForm()

    context = {
        'authors': authors,
        'publishers': publishers,
        'book_form': book_form,
        'publisher_form': publisher_form,
        'author_form': author_form,
    }

    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u: u.groups.filter(name='Managers').exists(), login_url=reverse_lazy('login'))
def add_book_instance(request):
    template = loader.get_template('manager/add_book_instance.html')
    books = Book.objects.all()
    
    if request.method == 'POST':
        book_instance_form = BookInstanceForm(request.POST)
        selected_book = None

        if book_instance_form.is_valid():
            if request.POST.get('book_id') is not None:
                selected_book = get_object_or_404(Book, pk=request.POST.get('book_id'))
            
            book_instance = book_instance_form.save(commit=False)
            status = book_instance_form.cleaned_data['status']
            book_instance.status = status
            book_instance.book = selected_book
            book_instance.save()

            return redirect('book_instances')

    else:
        book_instance_form = BookInstanceForm()

    context = {
        'books': books,
        'book_instance_form': book_instance_form,
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u: not u.is_authenticated or u.groups.filter(name='Managers').exists(), login_url=reverse_lazy('login'))
def view_book_details(request, book_id):
    template = loader.get_template('manager/book_details.html')
    selected_book = Book.objects.get(pk=book_id)
    authors = Author.objects.all()
    publishers = Publisher.objects.all()

    if request.method == 'POST':
        book_form = BookForm(data=request.POST, instance=selected_book)

        selected_author = None   
        selected_publisher = None   
        
        if book_form.is_valid():
            if request.POST.get('author_id') is not None:
                selected_author = get_object_or_404(Author, pk=request.POST.get('author_id'))
           
            if request.POST.get('publisher_id') is not None:
                selected_publisher = get_object_or_404(Publisher, pk=request.POST.get('publisher_id'))
        

            if book_form.is_valid():
                book = book_form.save(commit=False)
                book.author = selected_author
                book.publisher = selected_publisher
                book.save()

                return redirect('manager_index')
        else:
            return redirect('view_book_details')

    else:
        book_form = BookForm(instance=selected_book)

    context = {
        'book': selected_book,
        'authors': authors,
        'publishers': publishers,
        'book_form': book_form,
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u: not u.is_authenticated or u.groups.filter(name='Managers').exists(), login_url=reverse_lazy('login'))
def view_book_instance_details(request, bookinstance_id):
    template = loader.get_template('manager/book_instance_details.html')
    selected_book_instance = BookInstance.objects.get(pk=bookinstance_id)
    books = Book.objects.all()
    if request.method == 'POST':
        book_instance_form = BookInstanceForm(request.POST, instance=selected_book_instance)
        selected_book = None

        print(book_instance_form.is_valid())
        if book_instance_form.is_valid():
            if request.POST.get('book_id') is not None:
                selected_book = get_object_or_404(Book, pk=request.POST.get('book_id'))
            
            book_instance = book_instance_form.save(commit=False)
            book_instance.book = selected_book
            book_instance.save()

            return redirect('book_instances')

    else:
        book_instance_form = BookInstanceForm(instance=selected_book_instance)

    context = {
        'book_instance_form': book_instance_form,
        'instance': selected_book_instance,
        'books': books,
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u: u.groups.filter(name='Managers').exists(), login_url=reverse_lazy('login'))
def change_password(request):
    template = loader.get_template('manager/change_password.html')
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
                        return redirect('manager_index')
            else:
                form.add_error('current_password', "Password is incorrect")

    else:
        form = ResetPasswordForm()
    context = {
        'reset_password_form': form,
    }
    return HttpResponse(template.render(context, request))

def delete_book(request, book_id):
    selected_book = Book.objects.get(pk=book_id)
    book_instances = BookInstance.objects.filter(book=selected_book)
    for instance in book_instances:
        instance.delete()
    selected_book.delete()
    return redirect("manager_index")
        
        
