from django.template import loader
from django.template.response import TemplateResponse
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
# Create your views here.

@user_passes_test(lambda u: not u.is_authenticated or u.groups.filter(name='Users').exists(), login_url=reverse_lazy('login'))
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            books = Book.objects.filter(Q(title__icontains=query) | Q(author__in=Author.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))) )   
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        books = Book.objects.all()
        form = SearchForm()
    template = loader.get_template('catalog/books.html')
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
        'search_form': form,
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
            password = user_form.cleaned_data['password1']
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
            user_group = Group.objects.get(name='Users')
            user_group.user_set.add(user)
            user_group.save()
            LogEntry.objects.log_action(
                user_id=user.id,
                content_type_id=ContentType.objects.get_for_model(User).pk,
                object_id=user.id,
                object_repr=user.username,
                action_flag=ADDITION)
            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)         
                    return redirect("catalog_index")

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

@user_passes_test(lambda u: not u.is_authenticated or u.groups.filter(name='Users').exists(), login_url=reverse_lazy('login'))
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
            current_review = Review.objects.get(id=review.id)
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Review).pk,
                object_id=current_review.id,
                object_repr=current_review.book.title,
                action_flag=CHANGE,
                change_message="Added review \""+current_review.text+"\"")
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

@user_passes_test(lambda u: not u.is_authenticated or u.groups.filter(name='Users').exists(), login_url=reverse_lazy('login'))
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
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ContentType.objects.get_for_model(BookInstance).pk,
                    object_id=i.id,
                    object_repr=i.book.title,
                    action_flag=CHANGE,
                    change_message="Reserved Instance " + str(i.id))
                i.save()
                break
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@user_passes_test(lambda u: not u.is_authenticated or u.groups.filter(name='Users').exists(), login_url=reverse_lazy('login'))
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        
        if request.user.check_password('{}'.format(request.POST.get("current_password"))) == False:
            form.set_current_password_flag()

        if form.is_valid():
            user = request.user
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['password1']
            confirm_new_password = form.cleaned_data['password2']
            check_authentication = check_password(current_password, user.password)

            if check_authentication:
                user.set_password(new_password)   
                user.save()
                LogEntry.objects.log_action(
                    user_id=user.id,
                    content_type_id=ContentType.objects.get_for_model(User).pk,
                    object_id=user.id,
                    object_repr=user.username,
                    action_flag=CHANGE,
                    change_message="Changed password")
                login_user = authenticate(request=request, username=user.username, password=new_password)
                if user is not None:
                    if user.is_active:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        return redirect('profile')

    else:
        form = ResetPasswordForm()
    current_borrowed_books = request.user.profile.bookinstance_current_books.all()
    for book in current_borrowed_books:
        if book.status == 'a':
            book.past_profiles.add(book.current_profile)
            book.current_profile = None
            book.save()
    current_borrowed_books = request.user.profile.bookinstance_current_books.all()
    past_borrowed_books = Book.objects.filter(bookinstance__in=profile.bookinstance_set.all()).distinct()
    template = loader.get_template('catalog/profile.html')
    instances = BookInstance.objects.all()
    status_dictionary = dict()
    for b in past_borrowed_books:
        status = 'r'
        for i in instances:
            if i.book.isbn == b.isbn:
                if i.status == 'a':
                    status = 'a'
        status_dictionary[b] = status
    context = {
        'reset_password_form': form,
        'current_borrowed_books': current_borrowed_books,
        'past_borrowed_books': past_borrowed_books,
        'status_dictionary': status_dictionary,
    }
    return HttpResponse(template.render(context, request))
