from django.urls import path
from . import views

urlpatterns = [
    path('', views.media, name='media'),
    path('album_singles/<album_id>', views.album_singles,
         name='album_singles'),
    path('single_content/<single_id>', views.single_content,
         name='single_content'),
    path('add_comment', views.add_comment,
         name='add_comment'),
    path('get_comments', views.get_comments,
         name='get_comments'),

]
