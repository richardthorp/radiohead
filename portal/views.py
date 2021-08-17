from datetime import datetime
from time import sleep
import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from profiles.models import Profile

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_public_key = settings.STRIPE_PUBLIC_KEY


# This view ensures that the user is logged in as well as redirecting
# logged in users with active subscriptions
def portal_info(request):
    if str(request.user) != 'AnonymousUser':
        if request.user.profile.subscription_status == 'active':
            return redirect(reverse('portal_content'))
    return render(request, 'portal/portal_info.html')


# Generate or find Stripe Customer and create a new Subscription
@login_required
def create_portal_customer(request):
    email = request.user.email
    user_profile = request.user.profile
    try:
        # If the user profile already has a stripe customer ID, try to
        # retrieve the Stripe customer object associated with the profile
        if user_profile.portal_cust_id:
            try:
                customer = stripe.Customer.retrieve(
                    user_profile.portal_cust_id
                )
                # If the customer object has been deleted on Stripe, create a
                # new stripe customer object
                if 'deleted' in customer.keys():
                    customer = stripe.Customer.create(email=email)

            # Stripe failed to retrieve the customer object
            except Exception:
                customer = stripe.Customer.create(email=email)

        # No customer ID attached to profile - create a new Stripe
        # customer object
        else:
            customer = stripe.Customer.create(email=email)

        # Add the Stripe customer ID to the users profile model
        user_profile.portal_cust_id = customer.id
        user_profile.save()

        # If the user profile has a subscription ID, try to retrieve the
        # subscription from Stripe
        if user_profile.subscription_id:
            try:
                subscription = stripe.Subscription.retrieve(
                    user_profile.subscription_id
                    )
                # If the subscription is active, redirect user to
                # Portal Content
                if subscription.status == 'active':
                    return redirect(reverse('portal_content'))

            # If Stripe returns anything but an active subscription, delete the
            # Subscription ID on the user profile
                else:
                    user_profile.subscription_id = ""
                    user_profile.save()
            except Exception:
                user_profile.subscription_id = ""
                user_profile.save()

        # Create a new subscription for the user
        customer_id = request.user.profile.portal_cust_id
        price_id = settings.SUBSCRIPTION_PRICE_ID

        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent'],
            metadata={'email': request.user.email}
        )

        # Save the Subscription ID on the Profile model to use when retrieving
        # subscription
        user_profile.subscription_id = subscription.id
        user_profile.save()

        context = {
            'subscription_id': subscription.id,
            'client_secret': (subscription.latest_invoice.
                              payment_intent.client_secret),
            'stripe_public_key': stripe_public_key,
            'portal_price': settings.PORTAL_PRICE,
        }

        return render(request, 'portal/portal_sign_up.html', context)

    except Exception as e:
        print(e)
        messages.error(request, 'Sorry, there was an issue generating the new subscription, \
            "please try again later')
        return redirect(reverse('portal_info'))


# Collect card details and process payment
# (payment processed in portal-payment.js and stripe-elements.js)
# def portal_sign_up(request):
#     context = {
#         'client_secret': request.session.get('clientSecret'),
#         'subscription_id': request.session.get('requestsubscriptionId'),
#         # 'portal_price': str(settings.PORTAL_PRICE),
#         'portal_price': 'HAHA',
#     }
#     # print('SUB ID: ', request.session.get('requestsubscriptionId'))
#     return render(request, 'portal/portal_sign_up.html', context)


def update_payment_card(request):
    # Get the customer object
    user_profile = request.user.profile
    customer = stripe.Customer.retrieve(
        user_profile.portal_cust_id
    )
    # Create a new payment intent
    intent = stripe.SetupIntent.create(
        customer=customer['id']
    )
    context = {
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'portal/update_payment_card.html', context)


def set_default_card(request):
    user_profile = request.user.profile
    payment_method_id = request.POST['payment_method_id']
    subscription_id = user_profile.subscription_id

    try:
        stripe.Subscription.modify(
            subscription_id,
            default_payment_method=payment_method_id
        )

        messages.success(request, 'Payment method updated')
        return HttpResponse(status=200)
    except Exception:
        messages.error(request, 'Error updating card details, \
            please try again later.')
        return HttpResponse(status=500)


def cancel_subscription(request, subscription_id):
    try:
        # Cancel the subscription at the end of the current billing period
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
        )
        # Get the subscription end date and format it to render to message
        subscription_end_date = datetime.fromtimestamp(
            subscription.current_period_end
            )
        formatted_end_data = subscription_end_date.strftime("%b %d %Y")
        messages.success(request, f'Subscription Cancelled. \
            You may access the Portal until {formatted_end_data}')
        return redirect(reverse('profile'))
    except Exception as e:
        print(e)


# This view renders the actual portal content for subscribed users
@login_required
def portal_content(request):
    if request.user.profile.subscription_status == 'active':
        return render(request, 'portal/portal_content.html')
    else:
        # If the user doesn't have an active subscription status on their
        # profile, allow 5 seconds for the Stripe webhook to be sent to
        # update the profile
        attempt = 1
        active_subscription = False
        while attempt <= 5:
            sleep(1)
            print('ATTEMPT:', attempt)
            profile = Profile.objects.get(user=request.user)
            if profile.subscription_status == 'active':
                active_subscription = True
                break
            attempt += 1
        if active_subscription:
            return render(request, 'portal/portal_content.html')
        else:
            messages.error(request, 'Sorry, you must have an active \
                subscription to Portal to view this page.')
            return redirect(reverse('portal_info'))


@login_required
def reactivate_subscription(request, subscription_id):
    if request.user.profile.subscription_id == subscription_id:
        stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False
        )
        return redirect(reverse('profile'))
    else:
        messages.error(request, 'You can not reactivate this subscription')
        return redirect(reverse('profile'))

    # if not request.user.profile.subscription_status == 'active':
    #     # If the user doesn't have an active subscription status on their
    #     # profile, allow 5 seconds for the Stripe webhook to be sent to
    #     # update the profile
    #     attempt = 1
    #     while attempt <= 5:
    #         sleep(1)
    #         if request.user.profile.subscription_status == 'active':
    #             active_subscription = True
    #             break
    #         attempt += 1            # THIS WHOLE THING NEEDS A VALID SUBSCRIBER OUTCOME!!
    #     if active_subscription:
    #         return render(request, 'portal/portal_content.html')
    #     else:
    #         messages.error(request, 'You must have an active Portal \
    #             subscription to view this page')
    #         return redirect(reverse('portal_info'))
