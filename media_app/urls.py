from django.urls import path
from . import views

urlpatterns = [
    path('', views.media, name='media'),
    path('<slug:slug>/', views.album_singles,
         name='album_singles'),
    path('<slug:album_slug>/<slug:single_slug>/', views.single_content,
         name='single_content'),
    path('get_comments', views.get_comments,
         name='get_comments'),
    path('add_comment', views.add_comment,
         name='add_comment'),
    path('edit_comment', views.edit_comment,
         name='edit_comment'),
    path('delete_comment', views.delete_comment,
         name='delete_comment'),
    path('add_single', views.add_single,
         name='add_single'),
    path('edit_single/<slug:slug>', views.edit_single,
         name='edit_single'),
    path('delete_single/<slug:slug>', views.delete_single,
         name='delete_single'),
]
