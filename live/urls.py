from django.urls import path
from . import views

urlpatterns = [
    path('', views.live, name='live'),
]
