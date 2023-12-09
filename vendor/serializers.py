from rest_framework import serializers
from .models import Vendor, PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    # Rename 'id' to 'vendor_id'
    vendor = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Vendor
        fields = ['vendor','vendor_code','name','contact_details','address']
        # fields = '__all__'

# class VendorSerializer_2(serializers.ModelSerializer):
#     class Meta:
#         model = Vendor
#         fields = ['id']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    # Rename 'id' to 'po_id'
    po_id = serializers.IntegerField(source='id', read_only=True)
    # vendor_id = serializers.IntegerField(source='vendor.id', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['po_id', 'vendor', 'po_number', 'order_date', 'items', 'quantity', 'status']

class VendorPerformanceSerializer(serializers.ModelSerializer):
    vendor = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Vendor
        fields = ['vendor','name','on_time_delivery_rate','quality_rating','response_time','fulfilment_rate']
