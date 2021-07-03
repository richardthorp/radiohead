from django.shortcuts import render
from .models import Album, Product


# Create your views here.
def shop(request):
    context = {
        'albums': Album.objects.all(),
        'products': Product.objects.all()
    }
    return render(request, 'shop/shop.html', context)
