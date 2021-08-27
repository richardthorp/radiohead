from django.contrib import admin

from .models import Order, ProductOrderLineItem, AlbumOrderLineItem


class ProductOrderLineItemAdminInline(admin.TabularInline):
    model = ProductOrderLineItem
    # verbose_name = 'Product Order Line Items'
    fields = ('order', 'product', 'size', 'quantity', 'lineitem_total')
    readonly_fields = ('lineitem_total',)


class AlbumOrderLineItemAdminInline(admin.TabularInline):
    model = AlbumOrderLineItem
    # verbose_name = 'Albums Order Line Items'
    fields = ('order', 'album', 'format', 'quantity', 'lineitem_total')
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (AlbumOrderLineItemAdminInline, ProductOrderLineItemAdminInline,)
    readonly_fields = ('order_number',
                       'date',
                       'delivery_cost',
                       'order_total',
                       'grand_total',
                       'original_bag',
                       'stripe_pid',)

    fields = ('order_number',
              'date',
              'profile',
              'email',
              'phone_number',
              'name',
              'address_line1',
              'address_line2',
              'town_or_city',
              'county',
              'postcode',
              'country',
              'delivery_cost',
              'order_total',
              'grand_total',
              'original_bag',
              'stripe_pid',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
