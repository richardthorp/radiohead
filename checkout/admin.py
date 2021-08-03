from django.contrib import admin

from .models import Order, OrderLineItem


class OrderLineItemProductAdminInline(admin.TabularInline):
    model = OrderLineItem
    verbose_name = 'Order Line Items (Products)'
    fields = ('order', 'product', 'size', 'quantity', 'lineitem_total')
    readonly_fields = ('lineitem_total',)


class OrderLineItemAlbumAdminInline(admin.TabularInline):
    model = OrderLineItem
    verbose_name = 'Order Line Items (Albums)'
    fields = ('order', 'album', 'format', 'quantity', 'lineitem_total')
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemProductAdminInline, OrderLineItemAlbumAdminInline,)
    readonly_fields = ('order_number',
                       'date',
                       'profile',
                       'delivery_cost',
                       'order_total',
                       'grand_total')

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
              'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
