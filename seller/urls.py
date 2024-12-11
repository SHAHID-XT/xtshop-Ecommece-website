from django.urls import path, include
from .views import *

urlpatterns = [
    path("view-sales/",sales_view,name="sales_views"),
    path("view-orders/",view_orders,name="orders_views"),
    path("download-labels/",download_labels,name="download_labels"),
    path("order-info/",view_order_details_seller,name="view_order_details_seller"),
    path("new-product/",add_new_product,name="new_product"),

]



