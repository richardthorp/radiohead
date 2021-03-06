from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add_to_bag/<slug:slug>', views.add_to_bag, name='add_to_bag'),
    path('update_bag/<product_type>/<slug:slug>', views.update_bag,
         name='update_bag'),
    path('remove_item/<product_type>/<slug:slug>', views.remove_item,
         name='remove_item'),
]
