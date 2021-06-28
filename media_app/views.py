from django.shortcuts import render
from shop.models import Album
from .models import Single


# Create your views here.
def media(request):
    context = {
        'albums': Album.objects.all()
    }
    return render(request, 'media_app/media.html', context)


def album_singles(request, album_id):
    context = {
        'singles': Single.objects.filter(album=album_id)
    }
    return render(request, 'media_app/album_singles.html', context)
