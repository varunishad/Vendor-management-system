from django.db import models

# Create your models here.
class Vendor(models.Model):
    vendor_code = models.CharField(max_length=50 ,unique=True)
    name = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=255)
    address = models.TextField()

    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating = models.FloatField(null=True,blank=True)
    response_time = models.FloatField(null=True, blank=True)
    fulfilment_rate = models.FloatField(null=True,blank=True)

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    po_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateField()
    items = models.TextField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50)
