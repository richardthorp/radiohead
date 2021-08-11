import stripe
from django.conf import settings
from django.shortcuts import render


def portal_info(request):
    return render(request, 'portal/portal_info.html')


def create_portal_customer(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    email = request.user.email
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    print('STRIPE KEY:', stripe_public_key)
    try:
        # Create a new customer object
        customer = stripe.Customer.create(
            email=email
            )
        # At this point, associate the ID of the Customer object with your
        # own internal representation of a customer, if you have one.
        # print(customer)

        customer_id = customer.id
        price_id = settings.SUBSCRIPTION_PRICE_ID

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
        print('IN THE EXCEPTION', e)


def portal_sign_up(request):
    context = {
        'client_secret': request.session.get('clientSecret'),
        'subscription_id': request.session.get('requestsubscriptionId'),
    }
    return render(request, 'portal/portal_sign_up.html', context)