from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('shop_detail/<item_type>/<item_id>', views.shop_detail,
         name='shop_detail'),
    path('add_product/<type>', views.add_product,
         name='add_product'),
]
