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
        'album': Album.objects.get(id=album_id),
        'singles': Single.objects.filter(album=album_id)
    }
    return render(request, 'media_app/album_singles.html', context)


def single_content(request, single_id):
    context = {
        'single': Single.objects.get(id=single_id)
    }
    return render(request, 'media_app/single_content.html', context)
