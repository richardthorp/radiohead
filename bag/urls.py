from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add_to_bag/<product_id>', views.add_to_bag, name='add_to_bag'),
]
