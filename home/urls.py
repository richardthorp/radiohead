from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin-hub/', views.admin_hub, name='admin_hub'),
]
