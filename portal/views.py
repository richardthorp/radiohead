import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required


# This view ensures that the user is logged in
def portal_info(request):
    return render(request, 'portal/portal_info.html')


@login_required
def create_portal_customer(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    email = request.user.email
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    try:
        user_profile = request.user.profile
        if not user_profile.portal_cust_id:
            # Create a new customer object
            customer = stripe.Customer.create(
                email=email
                )
            # Add the Stripe customer ID to the users profile model
            user_profile.portal_cust_id = customer.id
            user_profile.save()

        customer_id = request.user.profile.portal_cust_id
        price_id = settings.SUBSCRIPTION_PRICE_ID

        # CHECK HERE FOR AN ACITVE SUBSCRIPTION AND REDIRECT TO PORTAL CONTENT IF SO
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent'],
        )

        context = {
            'subscription_id': subscription.id,
            'client_secret': (subscription.latest_invoice.
                              payment_intent.client_secret),
            'stripe_public_key': stripe_public_key,

        }
        request.session['requestsubscriptionId'] = subscription.id,
        request.session['clientSecret'] = (subscription.latest_invoice.
                                           payment_intent.client_secret)

        return render(request, 'portal/portal_sign_up.html', context)

    except Exception as e:
        messages.error(request, 'Sorry, there was an issue generating the new subscription, \
            "please try again later')
        redirect(reverse('portal_info'))


def portal_sign_up(request):
    context = {
        'client_secret': request.session.get('clientSecret'),
        'subscription_id': request.session.get('requestsubscriptionId'),
    }
    return render(request, 'portal/portal_sign_up.html', context)
