from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from shop.models import Product, Album


# Data sent to the view_bag template via bag/contexts.py
def view_bag(request):
    return render(request, 'bag/view_bag.html')


def add_to_bag(request, slug):
    bag = request.session.get('bag', {})
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        if request.POST.get('format'):
            # Added item is an album
            album = get_object_or_404(Album, slug=slug)
            format = request.POST.get('format')

            if quantity < 1:
                messages.error(
                    request, 'You can not add less than one item to your bag!'
                    )
                return redirect(
                    reverse('shop_detail', args=['album', album.slug])
                    )

            if album.title in list(bag.keys()):
                # Album already exists in bag
                if format in bag[album.title]['items_by_format']:
                    # Format already exists in bag - update quantity
                    bag[album.title]['items_by_format'][format] += quantity
                    messages.success(
                        request,
                        (f"Updated quantity of '{album.title}' "
                         f"{format.capitalize()} to "
                         f"{ bag[album.title]['items_by_format'][format]}")
                    )
                else:
                    # Add new format to bag
                    bag[album.title]['items_by_format'][format] = quantity
                    messages.success(
                        request,
                        f"Added '{album.title}' "
                        f"{format.capitalize()} to your bag.")
            else:
                # Add new album to bag
                bag[album.title] = {
                    'type': 'album',
                    'items_by_format': {
                        format: quantity,
                    }
                }
                messages.success(
                    request,
                    f"Added '{album.title}' "
                    f"{format.capitalize()} to your bag.")

        elif request.POST.get('size'):
            # Added item is a sized product
            product = get_object_or_404(Product, slug=slug)
            size = request.POST.get('size')

            # Get friendly name to display in messages
            if size == 'S':
                friendly_size = 'Small'
            if size == 'M':
                friendly_size = 'Medium'
            if size == 'L':
                friendly_size = 'Large'

            if quantity < 1:
                messages.error(
                    request, 'You can not add less than one item to your bag!'
                    )
                return redirect(
                    reverse('shop_detail', args=['product', product.slug])
                    )

            if product.name in list(bag.keys()):
                # Product already exists in bag
                if size in bag[product.name]['items_by_size']:
                    # Size already exists in bag - update quantity
                    bag[product.name]['items_by_size'][size] += quantity
                    messages.success(
                        request,
                        (f"Updated quantity of {friendly_size} {product.name}"
                         f" to {bag[product.name]['items_by_size'][size]}")
                    )

                else:
                    # Add new size to bag
                    bag[product.name]['items_by_size'][size] = quantity
                    messages.success(
                        request,
                        f'Added {friendly_size} {product.name} to your bag.')
            else:
                # Add new product to bag
                bag[product.name] = {
                    'type': 'sized',
                    'items_by_size': {
                        size: quantity,
                    }
                }
                messages.success(
                    request,
                    f'Added {friendly_size} {product.name} to your bag.')
        else:
            # Added item is a non-sized product
            product = get_object_or_404(Product, slug=slug)
            if quantity < 1:
                messages.error(
                    request, 'You can not add less than one item to your bag!'
                    )
                return redirect(
                    reverse('shop_detail', args=['product', product.slug])
                    )

            if product.name in list(bag.keys()):
                # Product already exists in bag - update quantity
                bag[product.name] += quantity
                messages.success(
                    request,
                    f'Updated {product.name} quantity to {bag[product.name]}.')
            else:
                # Add new product to bag
                bag[product.name] = quantity
                messages.success(request, f'Added {product.name} to your bag.')

        request.session['bag'] = bag
        return redirect(reverse('view_bag'))

    else:  # Request method is not post, redirect request
        return redirect(reverse('shop'))


def update_bag(request, product_type, slug):
    bag = request.session.get('bag', {})
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity < 1:
            messages.error(
                request,
                'Click on the remove button to remove item from bag.'
                )
            return redirect(reverse('view_bag'))

        if product_type == 'cd' or product_type == 'vinyl':
            album = get_object_or_404(Album, slug=slug)
            bag[album.title]['items_by_format'][product_type] = quantity

        if product_type == 'S' or product_type == 'M' or product_type == 'L':
            product = get_object_or_404(Product, slug=slug)
            bag[product.name]['items_by_size'][product_type] = quantity

        if product_type == 'other':
            product = get_object_or_404(Product, slug=slug)
            bag[product.name] = quantity

        request.session['bag'] = bag
        messages.success(request, 'Item successfully updated in your bag.')
        return redirect(reverse('view_bag'))
    else:  # Request method is not post, redirect request
        return redirect(reverse('view_bag'))


def remove_item(request, product_type, slug):
    bag = request.session.get('bag', {})

    if product_type == 'cd' or product_type == 'vinyl':
        album = get_object_or_404(Album, slug=slug)
        del bag[album.title]['items_by_format'][product_type]
        # Ensure that the album is removed from the bag if no other
        # format types for the same album are in the bag
        if not bag[album.title]['items_by_format'].get('cd') and \
           not bag[album.title]['items_by_format'].get('vinyl'):
            del bag[album.title]
    if product_type == 'S' or product_type == 'M' or product_type == 'L':
        product = get_object_or_404(Product, slug=slug)
        del bag[product.name]['items_by_size'][product_type]
        # Ensure that the product is removed from the bag if no other
        # sizes for the same product are in the bag
        if not bag[product.name]['items_by_size'].get('S') and \
           not bag[product.name]['items_by_size'].get('M') and \
           not bag[product.name]['items_by_size'].get('L'):
            del bag[product.name]
    if product_type == 'other':
        product = get_object_or_404(Product, slug=slug)
        del bag[product.name]

    request.session['bag'] = bag
    messages.success(request, 'Item successfully removed from your bag.')
    return redirect(reverse('view_bag'))
