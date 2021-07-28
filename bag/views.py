from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from shop.models import Product, Album


# Data sent to the view_bag template via bag/contexts.py
def view_bag(request):
    return render(request, 'bag/view_bag.html')


def add_to_bag(request, product_id):
    if request.POST.get('format'):
        album = get_object_or_404(Album, pk=product_id)
        album_name = album.title
        format = request.POST.get('format')
        size = False
    else:
        product = get_object_or_404(Product, pk=product_id)
        product_name = product.name
        size = request.POST.get('size')
        album = False

    quantity = int(request.POST.get('quantity'))

    bag = request.session.get('bag', {})

    if album:
        if album_name in bag.keys():
            if format in bag[album_name].keys():
                bag[album_name][format] += quantity
            else:
                bag[album_name][format] = quantity
        else:
            bag[album_name] = {
                'type': 'album',
                format: quantity,
            }
    elif size:
        if product_name in bag.keys():
            if size in bag[product_name].keys():
                bag[product_name][size] += quantity
            else:
                bag[product_name][size] = quantity
        else:
            bag[product_name] = {
                'type': 'sized',
                size: quantity
            }
    else:
        if product_name in bag.keys():
            bag[product_name] += quantity
        else:
            bag[product_name] = quantity

    request.session['bag'] = bag
    messages.success(request, 'Item successfully added to your bag.')
    # return render(request, 'bag/view_bag.html')
    return redirect(reverse('view_bag'))


def update_bag(request, product_type, product_id):
    print(product_type)
    bag = request.session.get('bag', {})
    quantity = int(request.POST.get('quantity'))

    if product_type == 'cd' or product_type == 'vinyl':
        album = get_object_or_404(Album, pk=product_id)
        bag[album.title][product_type] = quantity

    if product_type == 'S' or product_type == 'M' or product_type == 'L':
        product = get_object_or_404(Product, pk=product_id)
        bag[product.name][product_type] = quantity

    if product_type == 'other':
        product = get_object_or_404(Product, pk=product_id)
        bag[product.name] = quantity

    request.session['bag'] = bag
    messages.success(request, 'Item successfully updated in your bag.')
    return redirect(reverse('view_bag'))


def remove_item(request, product_type, product_id):
    bag = request.session.get('bag', {})

    if product_type == 'cd' or product_type == 'vinyl':
        album = get_object_or_404(Album, pk=product_id)
        del bag[album.title][product_type]
        if not bag[album.title].get('cd') and \
           not bag[album.title].get('vinyl'):
            del bag[album.title]
    if product_type == 'S' or product_type == 'M' or product_type == 'L':
        product = get_object_or_404(Product, pk=product_id)
        del bag[product.name][product_type]
        if not bag[product.name].get('S') and \
           not bag[product.name].get('M') and \
           not bag[product.name].get('L'):
            del bag[product.name]
    if product_type == 'other':
        product = get_object_or_404(Product, pk=product_id)
        del bag[product.name]

    request.session['bag'] = bag
    messages.success(request, 'Item successfully removed from your bag.')
    return redirect(reverse('view_bag'))
