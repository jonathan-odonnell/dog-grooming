from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineItem, Order


@receiver(post_save, sender=OrderLineItem)
def update_totals_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_totals_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()


@receiver(post_delete, sender=Order)
def update_appointments_on_delete(sender, instance, **kwargs):
    """
    Update appointment on order delete
    """
    instance.appointments.update(reserved=False, confirmed=False)
