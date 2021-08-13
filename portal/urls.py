from django.urls import path
from . import views
from .webhooks import portal_webhook

urlpatterns = [
    path('', views.portal_info, name='portal_info'),
    path('create-portal-customer/', views.create_portal_customer,
         name='create_portal_customer'),
    path('portal_sign_up/', views.portal_sign_up,
         name='portal_sign_up'),
    path('portal_wh/', portal_webhook, name='portal_webhook'),
]