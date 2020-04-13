from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='books'),
    path('signup/', views.SignupView.as_view(), name='signup'),
]