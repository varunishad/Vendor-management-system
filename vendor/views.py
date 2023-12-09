from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Order deleted"}, status=status.HTTP_200_OK)

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        # Check if vendor_id is provided in the query parameters
        vendor_id = self.request.query_params.get('vendor_id', None)

        # Filter purchase order by vendor_id if provided
        queryset = PurchaseOrder.objects.all()
        if vendor_id is not None:
            queryset = queryset.filter(vendor_id=vendor_id)

        return queryset
    # queryset = PurchaseOrder.objects.all()

class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.order_by()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Order deleted"}, status=status.HTTP_200_OK)

class VendorPerformanceView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    # print('kwargs---', kwargs)
    lookup_field = 'id'

    # def get_object(self):
    #     print("id--31-",vendor_id)
    #     vendor_id = self.kwargs['id']
    #     print("id---",vendor_id)
    #     return self.queryset.get(id=vendor_id)


