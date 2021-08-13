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
            # If the user doesn't have an existing stripe customer ID,
            # create a new customer object
            print('SHOULDNT BE HERE')
            customer = stripe.Customer.create(
                email=email
                )
            # Add the Stripe customer ID to the users profile model
            user_profile.portal_cust_id = customer.id
            user_profile.save()

        customer_id = request.user.profile.portal_cust_id
        price_id = settings.SUBSCRIPTION_PRICE_ID

        # Check whether the user already has a subscription ID with Stripe
        if user_profile.subscription_id:
            try:
                subscription = stripe.Subscription.retrieve(
                    user_profile.subscription_id
                    )
                # If the subscription is active, redirect user to
                # Portal Content
                if subscription.status == 'active':
                    return redirect(reverse('shop'))  # NEED TO CHANGE THIS TO PORTAL CONTENT
            # If Stripe returns anything but an active subscription, delete the
            # Subscription ID on the user profile and create a new Subscription
                else:
                    user_profile.subscription_id = ""
                    user_profile.save()
            except Exception:
                user_profile.subscription_id = ""
                user_profile.save()

        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent'],
            metadata={'email': request.user.email}
        )

        # Save the Subscription ID on the Profile model to use for changing
        # or deleting subscription
        user_profile.subscription_id = subscription.id
        user_profile.save()

        context = {
            'subscription_id': subscription.id,
            'client_secret': (subscription.latest_invoice.
                              payment_intent.client_secret),
            'stripe_public_key': stripe_public_key,

        }
        # request.session['requestsubscriptionId'] = subscription.id,
        # request.session['clientSecret'] = (subscription.latest_invoice.
        #                                    payment_intent.client_secret)

        return render(request, 'portal/portal_sign_up.html', context)

    except Exception as e:
        print(e)
        messages.error(request, 'Sorry, there was an issue generating the new subscription, \
            "please try again later')
        return redirect(reverse('portal_info'))


def portal_sign_up(request):
    # context = {
    #     'client_secret': request.session.get('clientSecret'),
    #     'subscription_id': request.session.get('requestsubscriptionId'),
    # }
    # print('SUB ID: ', request.session.get('requestsubscriptionId'))
    return render(request, 'portal/portal_sign_up.html', context)
