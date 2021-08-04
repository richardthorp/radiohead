from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.conf import settings

from bag.contexts import bag_details

import stripe

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "Add items to your bag to checkout.")
        return redirect(reverse('shop'))

    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

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
