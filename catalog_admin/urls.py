from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('managers/',views.view_managers, name="view_managers")
]
