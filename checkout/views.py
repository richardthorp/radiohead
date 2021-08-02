from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import reverse, redirect


def checkout(request):
    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "Add items to your bag to checkout.")
        return redirect(reverse('shop'))

    return render(request, 'checkout/checkout.html')
