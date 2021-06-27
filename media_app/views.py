from django.shortcuts import render
from shop.models import Album


# Create your views here.
def media(request):
    context = {
        'albums': Album.objects.all()
    }
    return render(request, 'media_app/media.html', context)
