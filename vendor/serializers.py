from datetime import datetime
from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    vendor = serializers.IntegerField(source='id', read_only=True)  # Rename 'id' to 'vendor_id'
    class Meta:
        model = Vendor
        fields = ['vendor','vendor_code','name','contact_details','address']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    po_id = serializers.IntegerField(source='id', read_only=True)  # Rename 'id' to 'po_id'
    # vendor_id = serializers.IntegerField(source='vendor.id', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['po_id', 'vendor', 'po_number', 'order_date', 'expected_delivery_date','delivered_date', 'items', 'quantity', 'status', 'quality_rating','issue_date', 'acknowledgment_date']

    def validate_status(self, value):
        valid_statuses = ['PENDING', 'CANCELED', 'COMPLETED']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Status must be one of {', '.join(valid_statuses)}")

        return value

    def to_internal_value(self, data):
        if 'status' in data:        # Convert 'status' to uppercase before saving
            data['status'] = data['status'].upper()

        # Check if 'issue_date' is present in the request and contains only the date and not time
        if 'issue_date' in data and len(data['issue_date']) == 10:
            data['issue_date'] += " 00:00:00"

        # Convert issue_date to the desired format before validation
        # data['issue_date'] = self.format_issue_date(data.get('issue_date'))

        return super().to_internal_value(data)


class VendorPerformanceSerializer(serializers.ModelSerializer):
    vendor = serializers.IntegerField(source='id', read_only=True)

    # SerializerMethodField allows custom logic in the get_average_response_time method to compute the field value,
    average_response_time = serializers.SerializerMethodField()

    def get_average_response_time(self, vendor_obj):
        average_response_time = vendor_obj.average_response_time

        if average_response_time:
            # Convert timedelta to a human readable format
            days, seconds = average_response_time.days, average_response_time.seconds
            hours, remainder = divmod(seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            # Format the duration
            duration_string = ""
            if days:
                duration_string += f"{days} {'day' if days == 1 else 'days'} "
            if hours:
                duration_string += f"{hours} {'hour' if hours == 1 else 'hours'} "
            if minutes:
                duration_string += f"{minutes} {'minute' if minutes == 1 else 'minutes'}"

            return duration_string

        return None  # Return None if average_response_time is None

    class Meta:
        model = Vendor
        fields = ['vendor','name','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfilment_rate']


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
