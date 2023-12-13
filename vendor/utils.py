from django.db.models import Avg, F, ExpressionWrapper, fields
from .models import PurchaseOrder
from datetime import datetime
import pytz
from rest_framework import generics, status
from rest_framework.response import Response

def calculate_on_time_delivery_rate(instance):
    #Check if the status is being updated to 'completed'
    if instance.status == 'COMPLETED':
        vendor = instance.vendor

        #Count the no. of PO's delivered on or before delivery date
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status="COMPLETED", delivered_date__lte=instance.expected_delivery_date)
        required_completed_orders = completed_orders.count()

        #Calculate the on_time_delivery_rate
        if vendor.purchaseorder_set.filter(status='COMPLETED').exists():
            total_completed_orders = vendor.purchaseorder_set.filter(status="COMPLETED").count()
            on_time_deliery_rate = round((required_completed_orders/total_completed_orders) * 100.0, 2)
        else:
            #If there are no completed POs, set the On-Time Delivery Rate to 0
            on_time_deliery_rate = 0.0

        # Update the on_time_delivery_rate in the Vendor model
        vendor.on_time_delivery_rate = on_time_deliery_rate
        vendor.save()


def calculate_quality_rating_avg(instance):
    if instance.quality_rating:
        vendor = instance.vendor

        #Calculate the average of all quality_rating values for completed POs of the vendor.
        quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False).aggregate(avg_value=Avg('quality_rating'))
        quality_rating_avg = quality_rating_avg['avg_value']

        # Update the quality_rating_avg in the Vendor model
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()


def calculate_average_response_time(instance):
    if instance.acknowledgment_date:
        vendor = instance.vendor
        average_response_time = avg_response_time_calculation(vendor)

        # Update the average_response_time in the Vendor model
        vendor.average_response_time = average_response_time
        vendor.save()


def calculate_fulfillment_rate(instance):
    if instance.status != "PENDING":
        vendor = instance.vendor
        vendor_id = instance.vendor_id

        completed_orders = PurchaseOrder.objects.filter(vendor=vendor_id, status="COMPLETED").count()
        total_orders_issued = PurchaseOrder.objects.filter(vendor=vendor_id).count()

        fulfilment_rate = round((completed_orders/total_orders_issued) * 100.0, 2)

        vendor.fulfilment_rate = fulfilment_rate
        vendor.save()

def avg_response_time_calculation(vendor):
    # Calculate the Avg of time differences between acknowledgment_date and issue_date
    time_difference_avg = PurchaseOrder.objects.filter(vendor=vendor,acknowledgment_date__isnull=False).annotate(time_diff=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'),output_field=fields.DurationField())).aggregate(avg_time_diff=Avg('time_diff'))
    average_response_time = time_difference_avg['avg_time_diff']

    return average_response_time


def get_current_indian_time():
    #Get the current UTC time
    utc_now = datetime.utcnow()

    # Set the UTC time zone
    utc_timezone = pytz.timezone('UTC')
    utc_now = utc_timezone.localize(utc_now)

    # Convert to Indian Standard Time (IST)
    ind_timezone = pytz.timezone('Asia/Kolkata')
    curren_timezone = utc_now.astimezone(ind_timezone)

    return curren_timezone
