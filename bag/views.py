from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product, Album


def view_bag(request):
    return render(request, 'bag/view_bag.html')


def add_to_bag(request, product_id):
    # del request.session['bag']
    if request.POST.get('format'):
        album = get_object_or_404(Album, pk=product_id)
        album_name = album.title
        format = request.POST.get('format')
    else:
        product = get_object_or_404(Product, pk=product_id)
        product_name = product.name
        size = request.POST.get('size')
        product = True

    quantity = int(request.POST.get('quantity'))

    bag = request.session.get('bag', {})

    if album:
        if album_name in bag.keys():
            if format in bag[album_name].keys():
                bag[album_name][format] += quantity
            else:
                bag[album_name][format] = quantity
        else:
            print('SECOND')
            bag[album_name] = {
                format: quantity,
            }


    request.session['bag'] = bag
    print(request.session['bag'])

    return render(request, 'bag/view_bag.html')
    # return redirect('shop')
