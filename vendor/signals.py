from django.dispatch import receiver
from .models import PurchaseOrder, Vendor
from django.db.models.signals import post_save, post_delete
from .utils import calculate_on_time_delivery_rate, calculate_quality_rating_avg, calculate_average_response_time, calculate_fulfillment_rate

#update on_time_delivery_rate after deleteing or saving PO
@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, **kwargs):
    calculate_on_time_delivery_rate(instance)

#update quality_rating_avg after deleteing or saving PO
@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, **kwargs):
    calculate_quality_rating_avg(instance)

#update average_response_time after deleteing or saving PO
@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_average_response_time(sender, instance, **kwargs):
    calculate_average_response_time(instance)

#update fulfilment_rate after deleteing or saving PO
@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_fulfilment_rate(sender, instance, **kwargs):
    calculate_fulfillment_rate(instance)
