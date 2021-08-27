import json
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .webhook_handler import OrderWH_Handler


# Webhook function copied from Boutique Ado project
@require_POST
@csrf_exempt
def webhook(request):
    # Listen for webhooks from Stripe
    wh_secret = settings.STRIPE_CHECKOUT_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key, wh_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)

    # Set up webhook handler
    handler = OrderWH_Handler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.failed': handler.handle_payment_intent_failed,
    }

    # Get the event type from Stripe
    event_type = event['type']

    event_handler = event_map.get(event_type, handler.handle_event)

    response = event_handler(event)

    return response
