from django.urls import path
from . import views

urlpatterns = [
    path('', views.media, name='media'),
    path('album_singles/<album_id>', views.album_singles,
         name='album_singles'),
    path('single_content/<single_id>', views.single_content,
         name='single_content'),


]
