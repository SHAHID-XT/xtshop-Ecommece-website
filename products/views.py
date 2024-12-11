from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from auths.models import *
from auths.utils import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models import F
from django.conf import settings
from ecommerce.context_processors import global_variables
import json
import requests
from forex_python.converter import CurrencyRates
from urllib.parse import urlencode
from auths.utils import custom_redirct


def Home(request):
    maxprice = request.GET.get("maxprice", 50000)
    search = request.GET.get("qq", False)
    sortby = request.GET.get("sort", "Top")  # Default sort by 'Top'
    category = request.GET.get("category", False)
    brand = request.GET.get("brand", False)
    rating = request.GET.get("rating", False)
    page_number = request.GET.get("page", 1)

    # Filter products based on the provided parameters
    filters = {}
    if maxprice:
        filters["price__lte"] = int(maxprice)
    if category:
        filters["category__name"] = category
    if brand:
        filters["brand"] = brand

    if rating and rating != "0":
        # Filter products by average rating
        products_with_rating = Product.filter_by_average_rating(rating)

        # Add rating filter option to the filters dictionary
        filters["id__in"] = products_with_rating.values_list("id", flat=True)

    objects = Product.objects.filter(**filters)
    if search:
        # Use Q object to perform case-insensitive search on multiple fields
        objects = objects.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(brand__icontains=search)
            | Q(model_name__icontains=search)
            | Q(category__name__icontains=search)
            | Q(tags__icontains=search)
            | Q(special_featuers__icontains=search)
        )

    # Apply sorting
    if sortby == "Newest":
        objects = objects.order_by("-created_at")
    elif sortby == "Price":
        objects = objects.order_by("-price")

    elif sortby == "Top":
        # Annotate each product with the total number of orders
        objects = objects.annotate(num_orders=Count("orderitem"))
        # Order the products by the number of orders in descending order
        objects = objects.order_by("-num_orders")

    elif sortby == "Popular":
        objects = objects.annotate(num_views_count=Count("num_views"))
        objects = objects.order_by("-num_views")

    # Pagination
    p = Paginator(objects, 30)
    products = p.get_page(page_number)
    page_obj = products

    # Get top categories and brands
    top_categories = Product.get_all_categories()
    top_brands = Product.get_all_brands()
    return render(
        request,
        "index.html",
        {
            "products": products,
            "page_obj": page_obj,
            "top_categories": top_categories,
            "top_brands": top_brands,
            "maxprice": maxprice,
            "category": category,
            "brand": brand,
            "rating": rating,
            "sortby": sortby,  # sortby to template for displaying selected option
        },
    )


def productDetails(request, id, name):
    # Get the product object
    product = Product.objects.get(id=id)
    # Increment the num_views field by 1
    product.num_views += 1
    # Save the updated product object
    product.save(update_fields=["num_views"])
    # Render the product detail template with the updated product object
    return render(request, "product_detail.html", {"product": product})


@login_required(login_url="/login")
def cart_views(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_qunatity = sum(item.quantity for item in cart_items)
    total_discount = float(user_cart.total_mrp()) - float(user_cart.total_price())
    return render(
        request,
        "cart.html",
        context={
            "cart_items": cart_items,
            "total_price": total_price,
            "cart": user_cart,
            "total_discount": total_discount,
            "total_qunatity": total_qunatity,
        },
    )


@csrf_exempt
def add_to_cart(request, product_id):
    if request.method == "POST" and request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=user_cart, product=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse(data={"status": True}, safe=False)
    if not request.user.is_authenticated:
        return JsonResponse(data={"error": "login or register first..."}, safe=False)

    return JsonResponse(data={"error": True}, safe=False)


@csrf_exempt
def remove_from_cart_by_qty(request, cart_item_id):
    if request.method == "POST" and request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return JsonResponse(
            data={"status": True, "quantity": cart_item.quantity}, safe=False
        )

    return JsonResponse(data={"error": True}, safe=False)


@csrf_exempt
def add_from_cart_by_qty(request, cart_item_id):
    if request.method == "POST" and request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=cart_item_id)
        if cart_item.quantity >= 1:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse(
            data={"status": True, "quantity": cart_item.quantity}, safe=False
        )

    return JsonResponse(data={"error": True}, safe=False)


@csrf_exempt
def delete_product_from_cart(request, cart_item_id):
    if request.method == "POST" and request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        return JsonResponse(data={"status": True}, safe=False)

    return JsonResponse(data={"error": True}, safe=False)


@login_required(login_url="/login")
def order_view(request):
    orders = list(Order.objects.filter(user=request.user).order_by("-created_at"))
    return render(
        request,
        "orders.html",
        {
            "orders": orders,
        },
    )


@login_required(login_url="/login")
def create_paypal_payment(request):
    current_domain = request.scheme + "://" + request.META["HTTP_HOST"]
    if not request.user.is_authenticated:
        return render(request, "404.html", context={"error": "Something went wrong.."})
    cart = request.user.cart
    total_price = sum(
        item.product.price * item.quantity for item in cart.cartitem_set.all()
    )
    
    # cart.cartitem_set.all().delete()
    usd_total_price = round(total_price/83, 2)
    tranid = TemporaryTransaction.objects.create(price=total_price)
    TemporaryTransaction.delete_expired_transactions()
    tranid.save()
    preprocessor = global_variables(request)
    try:
        address = Address.objects.get(user=request.user)

    except:
        address = None

    try:
        if address.pincode and address.line1 and address.city and address.state:
            pass
        else:
            address = None

    except:
        address = None

    if not address:
        return custom_redirct(
            request, "/address?next=/checkout/&message=Address+Missing..."
        )

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {"currency_code": "USD", "value": f"{usd_total_price}"},
                "shipping": {
                    "name": {"full_name": f"{address.full_name}"},
                    "address": {
                        "address_line_1": f"{address.line1}",
                        "admin_area_2": f"{address.line2}, {address.landmark}",
                        "admin_area_1": f"{address.city}, {address.state}",
                        "postal_code": f"{address.pincode}",
                        "country_code": "IN",
                    },
                },
            }
        ],
        "application_context": {
            "brand_name": f"{preprocessor['website_name']}",
            "locale": "en-US",
            "landing_page": "BILLING",
            "shipping_preference": "SET_PROVIDED_ADDRESS",
            "user_action": "PAY_NOW",
            "return_url": f"{current_domain}/psucess/?returnUrl={tranid.transaction_id}",
            "cancel_url": f"{current_domain}/pcancel/?returnUrl={tranid.transaction_id}",
            "payment_method": {
                "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED",
                "payer_selected": "PAYPAL",
                "allowed_payment_method": "IMMEDIATE_PAY",
            },
        },
    }
    order_id = ""
    response = requests.post(
        "https://api-m.sandbox.paypal.com/v2/checkout/orders",
        headers=headers,
        data=json.dumps(data),
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
    )

    if response.status_code == 201:
        response_data = response.json()
        approval_url = next(
            link["href"] for link in response_data["links"] if link["rel"] == "approve"
        )
        order_id = response_data.get("id")
        tranid = TemporaryTransaction.objects.get(transaction_id=tranid.transaction_id)
        request.session["order_id"] = order_id
        tranid.order_id = order_id
        tranid.save()
        return redirect(approval_url)
    else:
        return render(request, "404.html", context={"error": "Something Went Wrong..."})


@login_required(login_url="/login")
def paypal_payment_return(request):
    single_order = None
    try:
        single_order = Product.objects.get(id=request.GET.get("p"))
    except:
        pass
    order_id = request.session.get("order_id")
    del request.session["order_id"]
    transid = TemporaryTransaction.objects.get(
        transaction_id=request.GET.get("returnUrl")
    )
    transid.save()

    response = requests.post(
        "https://api-m.sandbox.paypal.com/v1/oauth2/token",
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
    )

    access_token = response.json()["access_token"]

    cart = request.user.cart

    total_price = sum(
        item.product.price * item.quantity for item in cart.cartitem_set.all()
    )

    if single_order:
        total_price = single_order.price

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}",
        headers=headers,
    )

    if response.status_code == 200:
        payment_status = response.json()["status"]
        if payment_status == "APPROVED":

            if (
                float(transid.price) == float(total_price)
                and transid.order_id == order_id
            ):

                address = Address.objects.get(user=request.user)
                address.save()
                request.user.save()
                if not single_order:
                    order = Order.objects.create(
                        user=request.user,
                        total_price=total_price,
                        paypal_id=order_id,
                        address=address,
                    )

                    for item in cart.cartitem_set.all():
                        OrderItem.objects.create(
                            order=order, product=item.product, quantity=item.quantity
                        )

                    order.save()

                    [i.delete() for i in cart.cartitem_set.all()]
                else:
                    order = Order.objects.create(
                        user=request.user,
                        total_price=single_order.price,
                        paypal_id=order_id,
                        address=address,
                    )
                    order.save()
                    order_item = OrderItem.objects.create(
                        order=order, product=single_order, quantity=1
                    )
                    order_item.save()

            return custom_redirct(
                request,
                f"/order?id={order.id}&orderid={order.order_id}&message=Payment+Success",
            )
        else:
            transid.delete()
            render(
                request,
                "404.html",
                context={"error": "Payment Faild, please try again"},
            )
    else:
        return render(
            request, "404.html", context={"error": "Payment Faild, please try again"}
        )


@login_required(login_url="/login")
def create_single_paypal_payment(request, id):
    current_domain = request.scheme + "://" + request.META["HTTP_HOST"]
    if not request.user.is_authenticated:
        return render(request, "404.html", context={"error": "Something went wrong.."})

    product = Product.objects.get(id=id)
    total_price = product.price
    
    usd_total_price =round(total_price/83, 2)
    
    tranid = TemporaryTransaction.objects.create(price=total_price)
    TemporaryTransaction.delete_expired_transactions()
    tranid.save()
    preprocessor = global_variables(request)
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None

    try:
        if address.pincode and address.line1 and address.city and address.state:
            pass
        else:
            address = None

    except:
        address = None

    if not address:
        return custom_redirct(
            request, f"/address?next=/checkout/{id}&message=Address+Missing..."
        )

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {"currency_code": "USD", "value": f"{usd_total_price}"},
                "shipping": {
                    "name": {"full_name": f"{address.full_name}"},
                    "address": {
                        "address_line_1": f"{address.line1}",
                        "admin_area_2": f"{address.line2}, {address.landmark}",
                        "admin_area_1": f"{address.city}, {address.state}",
                        "postal_code": f"{address.pincode}",
                        "country_code": "IN",
                    },
                },
            }
        ],
        "application_context": {
            "brand_name": f"{preprocessor['website_name']}",
            "locale": "en-US",
            "landing_page": "BILLING",
            "shipping_preference": "SET_PROVIDED_ADDRESS",
            "user_action": "PAY_NOW",
            "return_url": f"{current_domain}/psucess/?returnUrl={tranid.transaction_id}&p={id}",
            "cancel_url": f"{current_domain}/pcancel/?returnUrl={tranid.transaction_id}",
            "payment_method": {
                "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED",
                "payer_selected": "PAYPAL",
                "allowed_payment_method": "IMMEDIATE_PAY",
            },
        },
    }
    order_id = ""
    response = requests.post(
        "https://api-m.sandbox.paypal.com/v2/checkout/orders",
        headers=headers,
        data=json.dumps(data),
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
    )
    if response.status_code == 201:
        response_data = response.json()
        approval_url = next(
            link["href"] for link in response_data["links"] if link["rel"] == "approve"
        )
        order_id = response_data.get("id")
        tranid = TemporaryTransaction.objects.get(transaction_id=tranid.transaction_id)
        request.session["order_id"] = order_id
        tranid.order_id = order_id
        tranid.save()

        return redirect(approval_url)
    else:
        return render(request, "404.html", context={"error": "Something Went Wrong..."})


@login_required(login_url="/login")
def order_details_view(request):
    id = request.GET.get("id")
    order_id = request.GET.get("orderid")
    order = Order.objects.filter(user=request.user, order_id=order_id, id=id).first()
    return render(
        request,
        "order_details.html",
        {
            "order": order,
        },
    )


def about_us_view(request):
    return render(request, "about-us.html")


def terms_condition_view(request):
    return render(request, "terms-condition.html")


def add_review(request):
    id = request.GET.get("id")
    orderid = request.GET.get("orderid")

    order = Order.objects.filter(id=id, order_id=orderid).first()

    if request.method == "POST":
        m = None
        productid = request.POST.get("productid")
        rating = request.POST.get("rate")
        review = request.POST.get("review")
        product = Product.objects.get(id=productid)
        try:
            t = Rating.objects.get(
                user=request.user, product=product, rating=rating, review=review
            )
            m = "Review Already exits, updated with new rating and reviews."
        except:
            t = Rating.objects.create(
                user=request.user, product=product, rating=rating, review=review
            )
        t.review = review
        t.rating = rating

        t.save()
        return redirect(f"/orders/message={m if m else 'Review Added..'}")

    return render(request, "add_review.html", {"order": order})
