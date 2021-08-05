from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AlbumOrderLineItem, ProductOrderLineItem


@receiver(post_save, sender=AlbumOrderLineItem)
def update_total_on_save_album_in_order(sender, instance, created, **kwargs):
    # Update order total when an Album line item is created or updated

    instance.order.update_total()


@receiver(post_delete, sender=AlbumOrderLineItem)
def update_total_on_delete_album_in_order(sender, instance, **kwargs):
    # Update order total when an Album line item is deleted

    instance.order.update_total()


@receiver(post_save, sender=ProductOrderLineItem)
def update_total_on_save_product_in_order(sender, instance, created, **kwargs):
    # Update order total when a Product line item is created or updated

    instance.order.update_total()


@receiver(post_delete, sender=ProductOrderLineItem)
def update_total_on_delete_product_in_order(sender, instance, **kwargs):
    # Update order total when a Product line item is deleted

    instance.order.update_total()
