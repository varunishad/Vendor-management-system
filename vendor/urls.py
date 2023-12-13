from django.urls import path
from .views import VendorListCreateView, VendorRetrieveUpdateDeleteView, PurchaseOrderCreateView, PurchaseOrderListView, PurchaseOrderRetrieveUpdateDeleteView, VendorPerformanceView, AcknowledgePurchaseOrderView

urlpatterns = [
    path('vendors/',VendorListCreateView.as_view(), name ='vendor-list-create'),
    path('vendors/<int:id>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),
    path('purchase_orders/create/', PurchaseOrderCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/', PurchaseOrderListView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:id>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(), name='purchase-order-retrieve-update-delete'),
    path('vendors/<int:id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),
]
