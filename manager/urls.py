from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='manager_index'),
    path('bookinstances/',views.book_instances, name="book_instances"),
    path('addbook/',views.add_book, name="add_book"),
    path('changepassword/',views.change_password, name="manager_change_password")
]
