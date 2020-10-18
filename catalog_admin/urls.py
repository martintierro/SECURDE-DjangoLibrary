from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('managers/',views.view_managers, name="view_managers"),
    path('managers/add/',views.add_manager, name="add_manager"),
    path('systemlogs/',views.system_logs, name="system_logs"),
    path('changepassword/',views.change_password, name="admin_change_password")
]
