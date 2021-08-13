# import json
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from profiles.models import Profile


@require_POST
@csrf_exempt
def portal_webhook(request):
    wh_secret = settings.STRIPE_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        signature = request.headers['stripe-signature']
        event = stripe.Webhook.construct_event(
            payload=request.body, sig_header=signature,
            secret=wh_secret)
        data = event['data']
        event_type = event['type']
    except Exception as e:
        print('WE HIT THE EXCEPT')
        return e

    data_object = data['object']

    if event_type == 'customer.subscription.created':
        # print(data)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    elif event_type == 'customer.subscription.updated':
        # If the user has not completed the subscription payment within 23
        # hours, the subscription object expires -
        # delete the subscription object
        # if data_object['status'] == 'incomplete_expired':
        #     stripe.SubscriptionItem.delete(
        #         data_object['id'],
        #         )

        user = User.objects.get(email=data_object['metadata']['email'])
        if data_object['status'] == 'active':
            # The subscription is active - set the the user profile
            # subsctiption_status to active to allow access to Portal
            # try:
            #     profile = Profile.objects.get(
            #         portal_cust_id=data_object['customer']
            #         )
            # except Profile.DoesNotExist:
            #     return HttpResponse(
            #         content='Error finding User in DB',
            #         status=500
            #     )
            user.profile.subscription_status = 'active'
            user.profile.save()
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    elif event_type == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        print('TESTING FAILED PAYMENT')
        # print(data)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    elif event_type == 'customer.subscription.deleted':
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        # print(data)
        print('SUB DELETED')

    # Set the default payment method for recurring charges
    elif event_type == 'invoice.payment_succeeded':
        if data_object['billing_reason'] == 'subscription_create':
            subscription_id = data_object['subscription']
            payment_intent_id = data_object['payment_intent']

            # Retrieve the payment intent used to pay the subscription
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Set the default payment method
            stripe.Subscription.modify(
                subscription_id,
                default_payment_method=payment_intent.payment_method
            )
            return HttpResponse(
                content=f'Webhook received: {event["type"]}. Default payment card set',
                status=200
            )

    elif event_type == 'invoice.paid':
        # profile.subscription_status = 'active'
        # profile.save()
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
    else:
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )