from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('shop_detail/<item_type>/<item_id>', views.shop_detail,
         name='shop_detail'),
]
