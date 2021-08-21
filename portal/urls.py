from django.urls import path
from . import views
from .webhooks import portal_webhook

urlpatterns = [
    path('', views.portal_info, name='portal_info'),
    path('content/', views.portal_content, name='portal_content'),
    path('add-portal-post/<post_type>', views.add_portal_post,
         name='add_portal_post'),
    path('subscribe-to-portal/', views.create_portal_customer,
         name='create_portal_customer'),
    path('save-customer-details/', views.save_customer_details,
         name='save_customer_details'),
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
    path('get_portal_comments', views.get_portal_comments,
         name='get_portal_comments'),
    path('add_portal_comment', views.add_portal_comment,
         name='add_portal_comment'),
    path('edit_portal_comment', views.edit_portal_comment,
         name='edit_portal_comment'),
    path('delete_portal_comment', views.delete_portal_comment,
         name='delete_portal_comment'),
]
