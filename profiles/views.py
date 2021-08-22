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
    # Check that the POST request contains the ProfileForm - If not, the
    # request came from update_default_card view so don't update default
    # profile info.
    if request.method == 'POST' and 'default_name' in request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            form = ProfileForm(instance=profile)
        else:
            messages.error(request,
                           'Form data is not valid, please try again.')
            context = {
                'form': form
            }
            return render(request, 'profiles/profile.html', context)
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
            formatted_end_date = subscription_end_date.strftime("%b %d %Y")

            # Check whether the user has cancelled the subscription - if so
            # render re-join button in profile template.
            if subscription.cancel_at_period_end is True:
                reactivation_link = True
            else:
                reactivation_link = False

            default_payment_method = stripe.PaymentMethod.retrieve(
                subscription.default_payment_method
            )
            default_payment_details = {
                'last_4': default_payment_method.card.last4,
                'exp_year': default_payment_method.card.exp_year,
                'exp_month': default_payment_method.card.exp_month
            }
            # customer = stripe.Customer.retrieve(profile.portal_cust_id)
        except Exception as e:
            default_payment_details = None
            formatted_end_date = None
            messages.error(request, f"We couldn't find a Portal subscription \
                for your profile. If you think this is an error, please \
                contact us at {settings.DEFAULT_FROM_EMAIL}")

        # Collate the subscription details to pass to template
        subscription_details = {
            'end_date': formatted_end_date,
            'portal_price': settings.PORTAL_PRICE,
            'subscription_id': profile.subscription_id
        }
    else:
        subscription_details = None
        default_payment_details = None
        reactivation_link = None

    context = {
        'profile': profile,
        'orders': profile.orders.all().order_by('-date'),
        'subscription_details': subscription_details,
        'default_payment_details': default_payment_details,
        'reactivation_link': reactivation_link,
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
