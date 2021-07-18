from django.urls import path
from . import views

urlpatterns = [
    path('<page>', views.live, name='live'),
    path('event_detail/<event_id>', views.event_detail, name='event_detail'),
]
