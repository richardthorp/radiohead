from time import sleep
import json
from django.http import HttpResponse
from .models import Order, AlbumOrderLineItem, ProductOrderLineItem
from shop.models import Product, Album
from profiles.models import Profile


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
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.amount / 100, 2)

        if intent.metadata.save_details == 'true':
            profile = Profile.objects.get(user__username=intent.metadata.user)
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
                        for size, quantity in bag_dict[item]['items_by_size'].items():
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
        return HttpResponse(content=f'Webhook received: {event["type"]}. '
                            f'Order created in webhook.')

    def handle_payment_intent_failed(self, event):
        # Handle a payment_intent.failed webhook
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
