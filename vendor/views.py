
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
from .utils import avg_response_time_calculation, get_current_indian_time
from django.db.models.signals import post_delete

# View or listing and creating vendors
class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()  # Retrieve all Vendor objects from the database
    serializer_class = VendorSerializer  # VendorSerializer to serialize and deserialize Vendor objects


#View for retrieving, updating, and deleting a specific vendor
class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'id'  # lookup field for retrieving a vendor by its ID

     # Override the destroy method to provide a custom response when a vendoris deleted
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Order deleted"}, status=status.HTTP_200_OK)


#View for creating purchase orders
class PurchaseOrderCreateView(generics.CreateAPIView):
    serializer_class = PurchaseOrderSerializer  # PurchaseOrderSerializer to serialize and deserialize Vendor objects

    # Override the create method to add custom validation and responses
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        vendor_id = data.get('vendor')
        order_date = data.get('order_date')
        expected_delivery_date = data.get('expected_delivery_date')
        issue_date = data.get('issue_date')[:10]  # takes only the date for comparison below
        acknowledgment_date = data.get('acknowledgment_date')
        po_status = data.get('status').upper()    # Converts the status to uppercase
        delivered_date = data.get("delivered_date")

        if not Vendor.objects.filter(pk=vendor_id).exists():
            return Response({"Vendor": f"No such vendor with vendor_id: {vendor_id}"}, status=status.HTTP_400_BAD_REQUEST)
        if order_date and expected_delivery_date and expected_delivery_date < order_date:
            return Response({"error": "Expected delivery date cannot be lesser than Order date"}, status=status.HTTP_400_BAD_REQUEST)
        if order_date and issue_date and issue_date > order_date:
            return Response({"error": "Issue date cannot be greater than Order date"}, status=status.HTTP_400_BAD_REQUEST)
        if po_status == "COMPLETED":
            if not delivered_date:
                return Response({"error": "The 'delivered_date' field is required when the status is 'COMPLETED'."}, status=status.HTTP_400_BAD_REQUEST)
            elif delivered_date < request.data['order_date']:
                    return Response({"error":"Delivered date cannot be lesser than the Order date."},status=status.HTTP_400_BAD_REQUEST)
        if po_status != "COMPLETED" and delivered_date:
            return Response({"error": "Since the status is not 'COMPLETED', the Delivered date has to be 'null'"}, status=status.HTTP_400_BAD_REQUEST)
        if acknowledgment_date:
            return Response({"message": "Please acknowledge the purchase order via acknowledge API first"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the purchase order to the database
        serializer.save()
        serialized_data = PurchaseOrderSerializer(serializer.instance).data

        return Response(serialized_data, status=status.HTTP_201_CREATED)


#View for listing all or specific purchase orders
class PurchaseOrderListView(generics.ListAPIView):
    serializer_class = PurchaseOrderSerializer

    # Override the get_queryset method to filter purchase orders based on vendor_id if provided
    def get_queryset(self):
        vendor_id = self.request.query_params.get('vendor_id', None)  # Check if vendor_id is provided in the query parameters (url)
        queryset = PurchaseOrder.objects.all()

        if vendor_id is not None:    # Filter purchase order by vendor_id if provided
            queryset = queryset.filter(vendor_id=vendor_id)

        return queryset


# View for retrieving, updating, and deleting a specific purchase order
class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'id'

    # Override the update method to add custom validation and responses
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        po_status = request.data['status'].upper()
        acknowledgment_date = request.data['acknowledgment_date']
        issue_date = request.data['issue_date']
        delivered_date = request.data['delivered_date']
        # purchase_order = instance.vendor

        if not instance.acknowledgment_date and acknowledgment_date:   # check if ordered has already been acknowledged and still some acknowledgment_date has been passed
            return Response({"message": "Please acknowledge the purchase order via acknowledge API first"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data['acknowledgment_date'] = instance.acknowledgment_date

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Check if status is being updated to 'completed'
        if 'status' in request.data and po_status == "COMPLETED":
            # Check if delivered_date is provided
            if not delivered_date:
                return Response({"error":"The 'delivered_date' field is required when updating the status to 'COMPLETED'."},status=status.HTTP_400_BAD_REQUEST)
            else:
                # Check if delivered_date is greater than the order_date
                if delivered_date < request.data['order_date']:
                    return Response({"error":"Delivered date cannot be lesser than the Order date."},status=status.HTTP_400_BAD_REQUEST)

        elif 'status' in request.data and po_status != "COMPLETED":
            #check if delivered_date provided without the status being 'completed'
            if delivered_date:
                return Response({"error":"Mention 'delivered_date' only when the order status is 'COMPLETED' else null."},status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)  # Call the base class update method to perform save
        return Response(serializer.data)

    # Override the destroy method to provide a custom response when a purchase order is deleted
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # To delete a specific purchase order w.r.t to the po_id passed
        self.perform_destroy(instance)
        post_delete.send(sender=PurchaseOrder, instance=instance)
        return Response({"message":"Order deleted"}, status=status.HTTP_200_OK)


#view for retrieving the performance of a specific vendor
class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'id'


#view for acknowledging a purchase order
class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    # Override the update method to handle the acknowledgment of a purchase order
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the order has already been acknowledged
        if instance.acknowledgment_date:
            return Response({"detail": "Purchase order already acknowledged."}, status=status.HTTP_400_BAD_REQUEST)

        dt = get_current_indian_time()
        current_datetime = dt.strftime('%Y-%m-%d %H:%M:%S')
        instance.acknowledgment_date = current_datetime  # Set acknowledgment_date to the current Indian timestamp
        instance.save()

        vendor = instance.vendor
        average_response_time = avg_response_time_calculation(vendor)

        vendor.average_response_time = average_response_time
        vendor.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

