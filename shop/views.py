from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Album, Product
from .forms import AddProductForm, AddAlbumForm
from itertools import chain


def shop(request):
    albums = Album.objects.all().order_by('-year')
    products = Product.objects.all()
    all_products = list(chain(albums, products))
    context = {
        'items': all_products,
        'all': True,
    }

    if request.POST:
        product_filter = request.POST.get('filter')
        if product_filter == 'music':
            context = {
                'items': Album.objects.all(),
                'music': True,
            }
        elif product_filter == 'clothing':
            context = {
                'items': Product.objects.filter(category='clothing'),
                'clothing': True,

            }
        elif product_filter == 'other':
            context = {
                'items': Product.objects.filter(category='other'),
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


def add_product(request, type):
    if type == 'album':
        item = 'album'
        form = AddAlbumForm()
    else:
        item = 'product'
        form = AddProductForm()

    context = {
        'form': form,
        'item': item,
    }

    return render(request, 'shop/add_product.html',
                  context)
