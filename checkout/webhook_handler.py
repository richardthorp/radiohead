from django.http import HttpResponse


# Webhook handler copied from Boutique Ado project
class StripeWH_Handler:
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        # Handle a generic/unknown/unexpected webhook
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        # Handle a payment_intent.succeeded webhook
        # intent = event.data.object

        # print(intent)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_failed(self, event):
        # Handle a payment_intent.failed webhook
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
