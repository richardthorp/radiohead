from django.shortcuts import render
from .models import Album, Product


# Create your views here.
def shop(request):
    context = {
        'albums': Album.objects.all(),
        'products': Product.objects.all()
    }
    return render(request, 'shop/shop.html', context)


def shop_detail(request, item_type, item_id):
    if item_type == 'album':
        context = {
            'album': Album.objects.get(id=item_id)
        }
        return render(request, 'shop/album.html', context)
    else:
        context = {
            'product': Product.objects.get(id=item_id)
        }
        return render(request, 'shop/product.html', context)
