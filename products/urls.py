from django.urls import path, include
from .views import *

urlpatterns = [
    path("", Home, name="home"),
    path("product/<str:id>/<str:name>", productDetails, name="product_detail"),
    path('cart/', cart_views, name='cart_view'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart-qty/<int:cart_item_id>/', remove_from_cart_by_qty, name='remove_from_cart_qty'),
    path('add-from-cart-qty/<int:cart_item_id>/', add_from_cart_by_qty, name='add_from_cart_qty'),

    path('delete-from-cart/<int:cart_item_id>/', delete_product_from_cart, name='delete_from_cart'),
    path('orders/', order_view, name='order_view'),
    path('psucess/', paypal_payment_return, name='psucess'),
    path("checkout/",create_paypal_payment,name="checkout"),
    path("checkout/<int:id>/",create_single_paypal_payment,name="single_checkout"),
    path('order/', order_details_view, name='order_detail_view'),
    path("about-us/",about_us_view,name="about-us"),
    path("terms-and-conditions/",terms_condition_view,name="terms-and-onditions"),
    path("create-review/",add_review,name="create_review"),
]
