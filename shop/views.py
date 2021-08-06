import ast
from itertools import chain
from django.shortcuts import render, reverse, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Album, Product
from .forms import AddProductForm, AddAlbumForm


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


# def shop_detail(request, item_type, item_id):
def shop_detail(request, item_type, slug):
    if item_type == 'album':
        album = Album.objects.get(slug=slug)
        # Check type of tracklist data as tracklists uploaded via JSON
        # fixtures come from DB as dict objects whereas tracklists added via
        # the 'AddAlbumForm' are returned as a str
        if isinstance(album.tracklist, str):
            tracklist = ast.literal_eval(album.tracklist)
        else:
            tracklist = album.tracklist

        context = {
            'album': album,
            'tracklist': tracklist,
        }
        return render(request, 'shop/album.html', context)
    else:
        context = {
            'product': Product.objects.get(slug=slug)
        }
        return render(request, 'shop/product.html', context)


@staff_member_required(login_url='account_login')
def add_product(request, item_type):
    if request.method == 'POST':
        if item_type == 'album':
            form = AddAlbumForm(request.POST, request.FILES)
        else:
            form = AddProductForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save()
            messages.success(request, f'{str(item)} added to store')
            return redirect(
                reverse('shop_detail', args=[item_type, item.slug])
                )
        else:
            messages.error(request, 'Error adding product, please try again.')
            context = {
                'form': form,
                'item_type': item_type,
            }
            return render(request, 'shop/add_product.html', context)

    if item_type == 'album':
        form = AddAlbumForm()
    else:
        form = AddProductForm()
    context = {
        'form': form,
        'item_type': item_type,
    }

    return render(request, 'shop/add_product.html', context)


@staff_member_required(login_url='account_login')
def edit_product(request, item_type, slug):
    tracklist = None
    if request.method == 'POST':
        if item_type == 'album':
            product = Album.objects.get(slug=slug)
            form = AddAlbumForm(request.POST, request.FILES, instance=product)

        else:
            product = Product.objects.get(slug=slug)
            form = AddProductForm(request.POST, request.FILES,
                                  instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated!')
            return redirect(reverse('shop_detail',
                                    args=[item_type, product.slug]))
        else:
            context = {
                'form': form,
                'item_type': item_type,
                'product': product,
                'tracklist': tracklist,
            }
            messages.error(request,
                           'Error with form data, please try again!')
            return render(request, 'shop/edit_product.html', context)

    if item_type == 'album':
        product = Album.objects.get(slug=slug)
        form = AddAlbumForm(instance=product)
        if isinstance(product.tracklist, str):
            tracklist = ast.literal_eval(product.tracklist)
        else:
            tracklist = product.tracklist

    else:
        product = Product.objects.get(slug=slug)
        form = AddProductForm(instance=product)

    context = {
        'form': form,
        'item_type': item_type,
        'product': product,
        'tracklist': tracklist,
        }
    return render(request, 'shop/edit_product.html', context)


@staff_member_required(login_url='account_login')
def delete_product(request, item_type, slug):
    if item_type == 'album':
        product = Album.objects.get(slug=slug)
        product_name = product.title
    else:
        product = Product.objects.get(slug=slug)
        product_name = product.name

    # if product.image:
    #     product.image.delete()
    product.delete()
    messages.success(request, f'{product_name} deleted from database.')
    return redirect(reverse('shop'))
