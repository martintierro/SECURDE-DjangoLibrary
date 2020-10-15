from django.template import loader
from django.template.response import TemplateResponse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from .models import *
from .forms import *

# Create your views here.


def index(request):
    template = loader.get_template('catalog/books.html')
    books = Book.objects.all()
    instances = BookInstance.objects.all()
    status_dictionary = dict()
    for b in books:
        status = 'r'
        for i in instances:
            if i.book.isbn == b.isbn:
                if i.status == 'a':
                    status = 'a'
        status_dictionary[b] = status

    context = {
        'books': books,
        'instances': instances,
        'status_dictionary': status_dictionary,
    }
    return HttpResponse(template.render(context, request))


class SignupView(View):
    user_form_class = UserForm
    profile_form_class = ProfileForm
    template_name = 'catalog/signup.html'

    # display blank form
    def get(self, request):
        user_form = self.user_form_class(None)
        profile_form = self.profile_form_class(None)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    # process from data
    def post(self, request):
        user_form = self.user_form_class(request.POST)
        profile_form = self.profile_form_class(request.POST)
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

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("index")

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })


def book_details(request, book_id):
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            profile = request.user.profile
            book = Book.objects.get(pk=book_id)
            review = form.save(commit=False)
            text = form.cleaned_data['text']
            review.text = text
            review.book = book
            review.profile = profile
            review.save()
            return redirect('book_details', book_id)

    else:
        form = ReviewForm()

    template = loader.get_template('catalog/book_details.html')
    selected_book = Book.objects.get(pk=book_id)
    num_total = BookInstance.objects.filter(book=selected_book).count()
    num_available = BookInstance.objects.filter(
        book=selected_book, status='a').count()
    num_reserved = BookInstance.objects.filter(
        book=selected_book, status='r').count()
    instances = BookInstance.objects.all()
    status = 'r'
    for i in instances:
        if i.book.isbn == selected_book.isbn:
            if i.status == 'a':
                status = 'a'
    reviews = Review.objects.filter(book=selected_book)
    context = {
        'book': selected_book,
        'num_total': num_total,
        'num_available': num_available,
        'num_reserved': num_reserved,
        'reviews': reviews,
        'status': status,
        'review_form': form
    }
    return HttpResponse(template.render(context, request))


def reserve_book(request, book_id):
    selected_book = Book.objects.get(pk=book_id)
    instances = BookInstance.objects.all()
    status_dictionary = dict()
    for i in instances:
        if i.book.isbn == selected_book.isbn:
            if i.status == 'a':
                i.status = 'r'
                if i.current_profile != None:
                    i.past_profiles.add(i.current_profile)
                i.current_profile = request.user.profile
                i.save()
                break
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def book_search(request, query):
    template = loader.get_template('catalog/books.html')
    books = Book.objects.filter(name__unaccent__icontains=query)
    authors = Author.objects.filter(
        firstname__unaccent__icontains=query, lastname__unaccent__icontains=query)
    for author in authors:
        books.append(Book.objects.get(author__exact=author))
    instances = BookInstance.objects.all()
    status_dictionary = dict()
    for b in books:
        status = 'r'
        for i in instances:
            if i.book.isbn == b.isbn:
                if i.status == 'a':
                    status = 'a'
        status_dictionary[b] = status

    context = {
        'books': books,
        'instances': instances,
        'status_dictionary': status_dictionary,
    }
    return HttpResponse(template.render(context, request))


def profile(request):
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
                        return redirect('profile')
            else:
                form.add_error('current_password', "Password is incorrect")

    else:
        form = ResetPasswordForm()
    current_borrowed_books = request.user.profile.bookinstance_current_books.all()
    past_borrowed_books = request.user.profile.bookinstance_set.all()
    template = loader.get_template('catalog/profile.html')
    context = {
        'reset_password_form': form,
        'current_borrowed_books': current_borrowed_books,
        'past_borrowed_books': past_borrowed_books
    }
    return HttpResponse(template.render(context, request))
