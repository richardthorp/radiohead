from django.shortcuts import render
from .models import Album, Product


# Create your views here.
def shop(request):
    context = {
        'albums': Album.objects.all().order_by('-year'),
        'products': Product.objects.all(),
        'all': True,
    }
    if request.POST:
        product_filter = request.POST.get('filter')
        if product_filter == 'music':
            context = {
                'albums': Album.objects.all(),
                'music': True,
            }
        elif product_filter == 'clothing':
            context = {
                'products': Product.objects.filter(category='clothing'),
                'clothing': True,

            }
        elif product_filter == 'other':
            context = {
                'products': Product.objects.filter(category='other'),
                'other': True,

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
