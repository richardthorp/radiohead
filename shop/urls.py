from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('<item_type>/<slug:slug>', views.shop_detail,
         name='shop_detail'),
    # path('add_product/<item_type>', views.add_product,
    #      name='add_product'),
    path('add_product/<item_type>/', views.add_product,
         name='add_product'),
    path('edit_product/<item_type>/<slug:slug>', views.edit_product,
         name='edit_product'),
    path('delete_product/<item_type>/<slug:slug>', views.delete_product,
         name='delete_product'),
]
