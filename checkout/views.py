import json
from django.shortcuts import render,HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.conf import settings
import stripe

from bag.contexts import bag_details
from .forms import OrderForm
from .models import Order, ProductOrderLineItem, AlbumOrderLineItem
from shop.models import Album, Product


# cache_checkout_data function copied from Boutique Ado project
@require_POST
def cache_checkout_data(request):
    try:
        # Get the payment ID from the client secret from Stripe
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Call the Payment_intent.modify method and add the form data
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag')),
            'save_details': request.POST.get('save_details'),
            'user': request.user,
        })

        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Something went wrong! Please try your payment again.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    bag = request.session.get('bag', {})
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
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
                    order_line_item = ProductOrderLineItem(
                        order=order,
                        product=Product.objects.get(name=item),
                        quantity=bag[item]
                    )
                    order_line_item.save()

                elif bag[item]['type'] == 'sized':
                    # Item is a sized-product
                    for size, quantity in bag[item]['items_by_size'].items():
                        item_details = {
                            'order': order,
                            'product': Product.objects.get(name=item),
                            'size': size,
                            'quantity': quantity,
                        }
                        print(item_details)
                        order_line_item = ProductOrderLineItem(**item_details)
                        order_line_item.save()

                elif bag[item]['type'] == 'album':
                    for format, quantity in (
                            bag[item]['items_by_format'].items()):

                        item_details = {
                                'order': order,
                                'album': Album.objects.get(title=item),
                                'format': format,
                                'quantity': quantity,
                            }
                        order_line_item = AlbumOrderLineItem(**item_details)
                        order_line_item.save()

                elif bag[item]['type'] == 'album':
                    # Item is an album
                    if 'cd' in bag[item]:
                        format = 'cd'
                    else:
                        format = 'vinyl'

                    item_details = {
                        'order': order,
                        'album': Album.objects.get(title=item),
                        'format': format,
                        'quantity': bag[item][format]
                    }
                    order_line_item = AlbumOrderLineItem(**item_details)
                    order_line_item.save('album')

            # Check if user checked the 'save_details' box
            if 'save_details' in request.POST:
                request.session['save_details'] = True

            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        # Inavlid order form
        else:
            messages.error(request, ('There is an issue with your information,'
                                     ' please check the form and try again.'))
            print(order_form.errors)

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


def checkout_success(request, order_number):
    if 'bag' in request.session:
        del request.session['bag']

    if 'save_details' in request.session:
        pass

    context = {
        'order': Order.objects.get(order_number=order_number),
    }
    return render(request, 'checkout/checkout_success.html', context)
