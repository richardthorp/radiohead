from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.conf import settings
import stripe

from bag.contexts import bag_details
from .forms import OrderForm
from .models import Order, OrderLineItem
from shop.models import Album, Product


def checkout(request):
    bag = request.session.get('bag', {})
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    print(bag)
    if request.method == 'POST':
        form_data = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'address_line1': request.POST['address_line1'],
            'address_line2': request.POST.get('address_line2'),
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST.get('county'),
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item in bag:
                if type(bag[item]) is int:
                    # Item is non-sized product
                    order_line_item = OrderLineItem(
                        order=order,
                        product=Product.objects.get(name=item),
                        quantity=bag[item]
                    )
                    order_line_item.save('product')

                elif bag[item]['type'] == 'sized':
                    # Item is a sized-product
                    if 'S' in bag[item]:
                        size = 'S'
                    elif 'M' in bag[item]:
                        size = 'M'
                    else:
                        size = 'L'

                    item_details = {
                        'order': order,
                        'product': Product.objects.get(name=item),
                        'size': size,
                        'quantity': bag[item][size]
                    }
                    order_line_item = OrderLineItem(**item_details)
                    order_line_item.save('product')

                elif bag[item]['type'] == 'album':
                    # Item is an album
                    if 'cd' in bag[item]:
                        format = 'cd'
                    else:
                        format = 'vinyl'
                    # album = Album.objects.get(title=item)
                    item_details = {
                        'order': order,
                        'album': Album.objects.get(title=item),
                        'format': format,
                        'quantity': bag[item][format]
                    }
                    order_line_item = OrderLineItem(**item_details)
                    order_line_item.save('album')

            # Check if user checked the 'save_details' box
            if 'save_details' in request.POST:
                # Add save details logic here
                pass
        else:
            print(order_form.errors)


# {'Wind up me window T-shirt - Black': {
#       'type': 'sized',
#       'M': 1,
#       'S': 1
# },
# 'In Rainbows 1000 piece jigsaw': 1,
# 'A Moon Shaped Pool': {
#       'type': 'album',
#       'cd': 1,
#       'vinyl': 1},
# 'In Rainbows': {
#       'type': 'album',
#       'vinyl': 1}}

    # GET REQUEST
    if not bag:
        messages.error(request, "Add items to your bag to checkout.")
        return redirect(reverse('shop'))

    stripe.api_key = stripe_secret_key
    current_bag = bag_details(request)
    bag_total = current_bag['grand_total']
    stripe_total = round(bag_total * 100)

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency='gbp',
        metadata={'integration_check': 'accept_a_payment'},
        )

    client_secret = intent['client_secret']

    form = OrderForm()

    context = {
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': client_secret,
    }

    return render(request, 'checkout/checkout.html', context)
