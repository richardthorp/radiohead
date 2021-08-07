from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import Order
from .forms import ProfileForm


@login_required
def profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
        # else:
        #     context = {
        #         'profile': profile,
        #         'orders': profile.orders.all().order_by('-date'),
        #         'form': form,
        #     }
        #     return render(request, 'profiles/profile.html', context)

    context = {
        'profile': profile,
        'orders': profile.orders.all().order_by('-date'),
        'form': form,
    }

    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    order = Order.objects.get(order_number=order_number)

    context = {
        'order_history': True,
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)