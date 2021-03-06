import json
import stripe
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.conf import settings

from bag.contexts import bag_details
from shop.models import Album, Product
from profiles.forms import ProfileForm
from profiles.models import Profile
from .models import Order, ProductOrderLineItem, AlbumOrderLineItem
from .forms import OrderForm


# cache_checkout_data function copied from Boutique Ado project
# CREDIT - Chris Zielinski
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
            'shop_order': 'true',
        })

        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request,
                       'Something went wrong! Please try your payment again.')
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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

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

            # Check if user checked the 'save_details' box
            if 'save_details' in request.POST:
                request.session['save_details'] = True

            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        # Inavlid order form
        else:
            messages.error(request, ('There is an issue with your information,'
                                     ' please check the form and try again.'))

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

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            form = OrderForm(initial={
                'name': profile.default_name,
                'email': request.user.email,
                'phone_number': profile.default_phone_number,
                'address_line1': profile.default_address_line1,
                'address_line2': profile.default_address_line2,
                'town_or_city': profile.default_town_or_city,
                'county': profile.default_county,
                'postcode': profile.default_postcode,
                'country': profile.default_country,
            })
        except Profile.DoesNotExist:
            form = OrderForm()
    else:
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

    if request.user.is_authenticated:
        profile = request.user.profile
        order = Order.objects.get(order_number=order_number)
        order.profile = profile
        order.save()

    if 'save_details' in request.session:
        profile_data = {
            'default_name': order.name,
            'default_email': order.email,
            'default_phone_number': order.phone_number,
            'default_street_address_1': order.address_line1,
            'default_street_address_2': order.address_line2,
            'default_town_or_city': order.town_or_city,
            'default_county': order.county,
            'default_postcode': order.postcode,
            'default_country': order.country,
        }
        form = ProfileForm(profile_data, instance=profile)
        if form.is_valid():
            form.save()

    context = {
        'order': Order.objects.get(order_number=order_number),
    }

    return render(request, 'checkout/checkout_success.html', context)
