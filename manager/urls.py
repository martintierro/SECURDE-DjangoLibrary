from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='manager_index'),
    path('bookinstances/',views.book_instances, name="book_instances"),
    path('addbook/',views.add_book, name="add_book"),
    path('addbookinstance/',views.add_book_instance, name="add_book_instance"),
    path('<int:book_id>/', views.view_book_details, name="view_book_details"),
    path('bookinstances/<str:bookinstance_id>/', views.view_book_instance_details, name="view_book_instance_details"),
    path('changepassword/',views.change_password, name="manager_change_password")
]
