from time import sleep
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from .models import Order, AlbumOrderLineItem, ProductOrderLineItem
from shop.models import Product, Album
from profiles.models import Profile


# Webhook handler modified from Boutique Ado project- CREDIT- Chris Zielinski
class OrderWH_Handler:
    def __init__(self, request):
        self.request = request

    def _send_order_confirmation_email(self, order):
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )

        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        # Handle a generic/unknown/unexpected webhook
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        # Handle a payment_intent.succeeded webhook
        intent = event.data.object
        # Check that the webhook is in relation to a shop order and
        # not from a subscription payment
        if intent.metadata.get('shop_order'):
            pid = intent.id
            bag = intent.metadata.bag
            billing_details = intent.charges.data[0].billing_details
            shipping_details = intent.shipping
            grand_total = round(intent.amount / 100, 2)

            if intent.metadata.save_details == 'true':
                profile = Profile.objects.get(
                    user__username=intent.metadata.user)
                profile.default_email = billing_details.email
                profile.default_name = shipping_details.name
                profile.default_phone_number = shipping_details.phone
                profile.default_address_line1 = shipping_details.address.line1
                profile.default_address_line2 = shipping_details.address.line2
                profile.default_town_or_city = shipping_details.address.city
                profile.default_county = shipping_details.address.state
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_country = shipping_details.address.country
                profile.save()

            order_exists = False
            attempt = 1
            while attempt <= 5:
                try:
                    order = Order.objects.get(
                        email__iexact=billing_details.email,
                        name__iexact=shipping_details.name,
                        phone_number__iexact=shipping_details.phone,
                        address_line1__iexact=shipping_details.address.line1,
                        address_line2__iexact=shipping_details.address.line2,
                        town_or_city__iexact=shipping_details.address.city,
                        county__iexact=shipping_details.address.state,
                        postcode__iexact=shipping_details.address.postal_code,
                        country__iexact=shipping_details.address.country,
                        grand_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid
                        )

                    order_exists = True
                    break

                except Order.DoesNotExist:
                    attempt += 1
                    sleep(1)

            if order_exists:
                self._send_order_confirmation_email(order)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]}. '
                            'Order is in database',
                    status=200
                )
            else:
                order = None
                try:
                    order = Order.objects.create(
                        email=billing_details.email,
                        name=shipping_details.name,
                        phone_number=shipping_details.phone,
                        address_line1=shipping_details.address.line1,
                        address_line2=shipping_details.address.line2,
                        town_or_city=shipping_details.address.city,
                        county=shipping_details.address.state,
                        postcode=shipping_details.address.postal_code,
                        country=shipping_details.address.country,
                        original_bag=bag,
                        stripe_pid=pid
                    )

                    bag_dict = json.loads(bag)
                    for item in bag_dict:
                        if type(bag_dict[item]) is int:
                            # Item is non-sized product
                            order_line_item = ProductOrderLineItem(
                                order=order,
                                product=Product.objects.get(name=item),
                                quantity=bag_dict[item]
                            )
                            order_line_item.save()

                        elif bag_dict[item]['type'] == 'sized':
                            # Item is a sized-product
                            items = bag_dict[item]['items_by_size'].items()
                            for size, quantity in items:
                                item_details = {
                                    'order': order,
                                    'product': Product.objects.get(name=item),
                                    'size': size,
                                    'quantity': quantity,
                                }
                                order_line_item = ProductOrderLineItem(
                                    **item_details)
                                order_line_item.save()

                        elif bag_dict[item]['type'] == 'album':
                            for format, quantity in (
                                    bag_dict[item]['items_by_format'].items()):

                                item_details = {
                                        'order': order,
                                        'album': Album.objects.get(title=item),
                                        'format': format,
                                        'quantity': quantity,
                                    }
                                order_line_item = AlbumOrderLineItem(
                                    **item_details)
                                order_line_item.save()

                except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(content=f'Webhook received: '
                                        f'{event["type"]}. Error: {e}',
                                        status=500)
            self._send_order_confirmation_email(order)
        return HttpResponse(content=f'Webhook received: {event["type"]}. '
                            f'Order created in webhook.')

    def handle_payment_intent_failed(self, event):
        # Handle a payment_intent.failed webhook
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
