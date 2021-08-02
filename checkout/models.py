import uuid
from django.db import models
from django.db.models import Sum
from django.conf import Settings

from profiles.models import Profile
from shop.models import Album, Product


class Order(models.Model):
    order_number = models.CharField(null=False, blank=False, max_length=32,
                                    editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name="orders")
    email = models.CharField(null=False, blank=False, max_length=150)
    name = models.CharField(null=False, blank=False, max_length=60)
    phone_number = models.CharField(null=False, blank=False, max_length=30)
    address_line1 = models.CharField(null=False, blank=False, max_length=80)
    address_line2 = models.CharField(max_length=80)
    town_or_city = models.CharField(null=False, blank=False, max_length=50)
    county = models.CharField(max_length=80)
    country = models.CharField(blank=False, null=False, max_length=80)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(null=False, decimal_places=2,
                                        max_digits=4)
    order_total = models.DecimalField(null=False, blank=False,
                                      decimal_places=2, max_digits=10)
    grand_total = models.DecimalField(null=False, blank=False,
                                      decimal_places=2, max_digits=10)

    def _generate_order_number(self):
        # Return a random number to attach to the order instance
        return uuid.uuid4().hex.upper()

    def update_total(self):
        self.order_total = self.lineitems.aggregate(
            Sum('lineitems_total'))['lineitems_total__sum']

        if self.order_total < Settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = Settings.STANDARD_DELIVERY_COST
        else:
            self.delivery_cost = 0

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        # If when the save method is called on the instance there is no order
        # number attached (the first time this instance has been saved),
        # attach an order number using the generate_order_method above.
        if not self.order_number:
            self.order_number = self.generate_order_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE, related_name='lineiems')
    product = models.ForeignKey(Product, null=True, blank=True,
                                on_delete=models.SET_NULL)
    size = models.CharField(max_length=1)
    album = models.ForeignKey(Album, null=True, blank=True,
                              on_delete=models.SET_NULL)
    format = models.CharField(max_length=5, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    lineitem_total = models.DecimalField(decimal_places=2, max_digits=6,
                                         null=False, blank=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        if self.product:
            self.lineitem_total = self.product.price * self.quantity
        else:
            if self.format == 'cd':
                self.lineitem_total = self.album.cd_price * self.quantity
            else:
                self.lineitem_total = self.album.vinyl_price * self.quantity

        super().save(*args, **kwargs)

    def __str__(self):
        if self.product:
            return (f'Line item in order {self.order.order_number} - '
                    f'{self.product.name}, {self.quantity}: '
                    f'{self.lineitem_total}')
        else:
            return (f'Line item in order {self.order.order_number} - '
                    f'{self.album.title}, {self.quantity}: '
                    f'{self.lineitem_total}')