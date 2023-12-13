from django.db import models

class Vendor(models.Model):
    vendor_code = models.CharField(max_length=50 ,unique=True) # A unique identifier for the vendor
    name = models.CharField(max_length=255) # Vendor's name
    contact_details = models.CharField(max_length=255) # Contact information of the vendor
    address = models.TextField() # Physical address of the vendor

    on_time_delivery_rate = models.FloatField(null=True, blank=True) # Tracks the percentage of on-time deliveries
    quality_rating_avg = models.FloatField(null=True, blank=True) # Average rating of quality based on purchase orders
    average_response_time = models.DurationField(null=True, blank=True) # Average time taken to acknowledge purchase orders
    fulfilment_rate = models.FloatField(null=True, blank=True) # Percentage of purchase orders fulfilled successfully


class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE) # Link to the Vendor model
    po_number = models.CharField(max_length=50, unique=True) # Unique number identifying the PO
    items = models.TextField() # Details of items ordered
    quantity = models.PositiveIntegerField() # Total quantity of items in the PO
    status = models.CharField(max_length=50) # Current status of the PO (e.g., pending, completed, canceled)
    order_date = models.DateField() # Date when the order was placed
    expected_delivery_date = models.DateField() # Expected delivery date of the order
    delivered_date = models.DateField(null=True, blank=True) # PO delivered date (to be updated later when the status changes to'completed')

    quality_rating = models.FloatField(null=True, blank=True) # Rating given to the vendor for this PO
    issue_date = models.DateTimeField() # Timestamp when the PO was issued to the vendor
    acknowledgment_date = models.DateTimeField(null=True, blank=True) # Timestamp when the vendor acknowledged the PO


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE) # Link to the Vendor model
    date = models.DateField() # Date of the performance record
    on_time_delivery_rate = models.FloatField() # Historical record of the on-time delivery rate
    quality_rating_avg = models.FloatField() # Historical record of the quality rating average
    average_response_time = models.FloatField() # Historical record of the average response time
    fulfilment_rate = models.FloatField() # Historical record of the fulfilment rate
