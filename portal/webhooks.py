import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string


@require_POST
@csrf_exempt
def portal_webhook(request):
    wh_secret = settings.STRIPE_PORTAL_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        signature = request.headers['stripe-signature']
        event = stripe.Webhook.construct_event(
            payload=request.body, sig_header=signature,
            secret=wh_secret)
        data = event['data']
        event_type = event['type']
    except Exception as e:
        return e

    data_object = data['object']

    if event_type == 'invoice.payment_succeeded':
        if data_object['billing_reason'] == 'subscription_create':
            # Customer has newly subscribed - Set the default payment method
            # for recurring charges and email them the Portal signup
            # confirmation
            subscription_id = data_object['subscription']
            payment_intent_id = data_object['payment_intent']
            metadata = data_object['lines']['data'][0]['metadata']
            # Send the email
            send_subscription_confirmation_email(metadata)
            # Retrieve the payment intent used to pay the subscription
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Set the default payment method
            stripe.Subscription.modify(
                subscription_id,
                default_payment_method=payment_intent.payment_method
            )
            return HttpResponse(
                content=f'Webhook received: {event["type"]}. '
                        f'Default payment card set',
                status=200
            )
        # Handle any other 'invoice.payment_succeeded' events
        return HttpResponse(
            content=f'Webhook received: {event["type"]}.',
            status=200
        )

    elif event_type == 'customer.subscription.updated':
        # This webhook event contains the current state of a customers
        # subscription. If the status is 'active', access is granted to the
        # portal content. Any other status will not allow access to Portal
        # content. The subscription status is saved to the users profile.
        user = User.objects.get(email=data_object['metadata']['email'])
        user.profile.subscription_status = data_object['status']
        user.profile.save()
        return HttpResponse(
            content=f"Webhook received: {event['type']}, {user.profile} "
                    f"subscription status is {data_object['status']}.",
            status=200
        )

    elif event_type == 'customer.subscription.deleted':
        # Subscriptions are set via the Stripe dashboard to be deleted
        # immediately after a recurring payment fails.
        # This webhook removes any Stripe subscription details from the user's
        # profile and sends the cancellation email
        metadata = data_object['metadata']
        user_email = metadata['email']
        user = User.objects.get(email=user_email)
        # Clear out any stripe id's from the user's profile
        user.profile.subscription_status = ''
        user.profile.portal_cust_id = ''
        user.profile.subscription_id = ''
        user.profile.save()
        # Email the user a cancellation confirmation
        send_subscription_cancelation_email(metadata)

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    # Handle any other webhook
    else:
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )


# Sends subscription confirmation email when a user signs up and pays.
# Called in the 'invoice.payment_succeeded' webhook handler
def send_subscription_confirmation_email(metadata):
    customer_email = metadata['email']
    customer_name = metadata['name']
    portal_price = settings.PORTAL_PRICE
    contact_email = settings.DEFAULT_FROM_EMAIL
    subject = render_to_string(
        'portal/confirmation_emails/portal_signup_confirmation_subject.txt',
    )

    body = render_to_string(
        'portal/confirmation_emails/portal_signup_confirmation_body.txt',
        {'name': customer_name,
         'contact_email': contact_email,
         'portal_price': portal_price}
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email]
    )


# Sends subscription cancelation email when a user either cancels their
# subscription or the subscription payments are not fulfilled.
# Called in the 'customer.subscription.deleted' webhook handler
def send_subscription_cancelation_email(metadata):
    customer_email = metadata['email']
    customer_name = metadata['name']
    contact_email = settings.DEFAULT_FROM_EMAIL
    subject = render_to_string(
        'portal/confirmation_emails/portal_cancellation_subject.txt',
    )

    body = render_to_string(
        'portal/confirmation_emails/portal_cancellation_body.txt',
        {'name': customer_name,
         'contact_email': contact_email}
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email]
    )
