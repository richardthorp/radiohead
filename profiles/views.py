import stripe
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from checkout.models import Order
from .forms import ProfileForm


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
    if profile.subscription_status == 'active':
        # Get the Subscription and Payment objects from Stripe
        try:
            subscription = stripe.Subscription.retrieve(
                profile.subscription_id
            )
            # Get the subscription end date and format it to render to template
            subscription_end_date = datetime.fromtimestamp(
                subscription.current_period_end
                )
            formatted_end_data = subscription_end_date.strftime("%b %d %Y")
            default_payment_method = stripe.PaymentMethod.retrieve(
                subscription.default_payment_method
            )
            default_payment_details = {
                'last_4': default_payment_method.card.last4,
                'exp_year': default_payment_method.card.exp_year,
                'exp_month': default_payment_method.card.exp_month
            }
            # customer = stripe.Customer.retrieve(profile.portal_cust_id)
        except Exception:
            messages.error(request, f"We couldn't find a Portal subscription \
                for your profile. If you think this is an error, please \
                contact us at {settings.DEFAULT_FROM_EMAIL}")

        # Collate the subscription details to pass to template
        subscription_details = {
            'end_date': formatted_end_data,
            'portal_price': settings.PORTAL_PRICE,
            'subscription_id': profile.subscription_id
        }
    else:
        subscription_details = None
        default_payment_details = None

    context = {
        'profile': profile,
        'orders': profile.orders.all().order_by('-date'),
        'subscription_details': subscription_details,
        'default_payment_details': default_payment_details,
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