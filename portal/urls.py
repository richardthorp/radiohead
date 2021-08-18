from django.urls import path
from . import views
from .webhooks import portal_webhook

urlpatterns = [
    path('', views.portal_info, name='portal_info'),
    path('content/', views.portal_content, name='portal_content'),
    path('subscribe-to-portal/', views.create_portal_customer,
         name='create_portal_customer'),
    path('portal_wh/', portal_webhook, name='portal_webhook'),
    path('update_payment_card/', views.update_payment_card,
         name='update_payment_card'),
    path('set_default_card/', views.set_default_card,
         name='set_default_card'),
    path('cancel_subscription/<subscription_id>', views.cancel_subscription,
         name='cancel_subscription'),
    path('reactivate_subscription/<subscription_id>',
         views.reactivate_subscription, name='reactivate_subscription'),
    path('portal_post_detail/<post_type>/<slug:slug>',
         views.portal_post_detail, name='portal_post_detail'),
]
