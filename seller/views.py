from django.shortcuts import render
from .utils import *
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import traceback


@seller_required
def sales_view(request):
    more_than_10_customer = None
    filter_date = "Year"
    try:
        filter_date = request.GET.get("by", "Year")
    except:
        pass
    today = datetime.now().date()
    end_date = today
    if filter_date:
        if filter_date == "Today":
            start_date = today
            end_date = today
        elif filter_date == "Week":
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif filter_date == "Month":
            start_date = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
        elif filter_date == "Year":
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)

    user = request.user
    seller_name = user.seller.name if hasattr(user, "seller") else None

    if not filter_date:
        # Get sales data for all time
        all_time_sales = OrderItem.objects.filter(
            Q(product__user=user) | Q(product__user__seller__name=seller_name)
        ).order_by("order__created_at")
    else:
        all_time_sales = OrderItem.objects.filter(
            Q(product__user=user) | Q(product__user__seller__name=seller_name),
            order__created_at__date__range=[start_date, end_date],
        ).order_by("order__created_at")

    all_time_order = list(set([f.order for f in (all_time_sales)]))[::-1]
    if int(len(all_time_order)) > 10:
        more_than_10_customer = (len(all_time_order)) - 10

    # Total products for all time
    total_products_all_time = Product.objects.filter(
        Q(user=user) | Q(user__seller__name=seller_name)
    ).count()

    # Total orders for all time
    total_orders_all_time = list(set(item.order for item in all_time_sales))

    total_orders_all_time = len(total_orders_all_time)

    all_time_customers = len(list(set([f.order.user for f in list(all_time_sales)])))

    # Sale products for all time
    sale_products_all_time = (
        OrderItem.objects.filter(
            Q(product__user=user) | Q(product__user__seller__name=seller_name)
        )
        .values("product__id", "product__name", "order")
        .annotate(total_quantity=Sum("quantity"))
    )

    # Total sale price for all time
    total_sale_price_all_time = sum(
        (item.product.price * item.quantity) for item in all_time_sales
    )

    return render(
        request,
        "view_sales.html",
        {
            "total_products_all_time": total_products_all_time,
            "total_orders_all_time": total_orders_all_time,
            "sale_products_all_time": sale_products_all_time,
            "total_sale_price_all_time": total_sale_price_all_time,
            "all_time_customers": all_time_customers,
            "all_time_order": all_time_order,
            "filter_date": filter_date,
            "more_than_10_customer": more_than_10_customer,
        },
    )


@seller_required
def view_orders(request):
    page_number = request.GET.get("page", 1)
    order_status = "Pending Labels"
    try:
        order_status = request.GET.get("status", "Pending Labels")
    except:
        pass
    filter_date = request.GET.get("by", "Year")

    today = datetime.now().date()
    user = request.user
    seller_name = user.seller.name if hasattr(user, "seller") else None

    if order_status == "Pending Labels":
        order_items = OrderItem.objects.filter(
            Q(order__label_generated=False),
            Q(product__user=user) | Q(product__user__seller__name=seller_name),
        ).order_by("-order__created_at")
    else:
        order_items = OrderItem.objects.filter(
            Q(order__status=order_status),
            Q(product__user=user) | Q(product__user__seller__name=seller_name),
        ).order_by("-order__created_at")
    orders = list(set([item.order for item in order_items]))[::-1]
    order_status_counts_info = return_my_order_info(seller_name, user)
    p = Paginator(orders, 30)
    orders = p.get_page(page_number)
    return render(
        request,
        "view_orders.html",
        {
            "orders": orders,
            "order_status_counts_info": order_status_counts_info,
            "order_status": order_status,
            "page_obj": orders,
        },
    )


@csrf_exempt
@seller_required
def download_labels(request):
    order_ids = [f for f in json.loads(request.GET.get("id", None)) if f]
    user = request.user
    seller_name = user.seller.name if hasattr(user, "seller") else None

    orders = Order.objects.filter(
        Q(orderitems__product__user__seller__name=seller_name)
        | Q(orderitems__product__user=user)
    ).distinct()

    print(len(orders))
    template_path = "label.html"
    context = {"orders": orders}
    response = HttpResponse(content_type="application/pdf")
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response["Content-Disposition"] = 'filename="Orders.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, default_css="", pagesize=(216, 432)
    )
    # if error then show some funny view
    if pisa_status.err:
        return redirect(f"/404/?message={pisa_status.err}")
    return response


def view_order_details_seller(request):
    try:
        user = request.user
        id = request.GET.get("id")
        orderid = request.GET.get("orderid")
        seller_name = user.seller.name if hasattr(user, "seller") else None
        order = Order.objects.filter(
            orderitems__product__user__seller__name=seller_name, order_id=orderid, id=id
        ).first()

        return render(
            request,
            "order_details.html",
            {
                "order": order,
            },
        )
    except Exception as e:
        print(e)
        return render(request, "404.html", {"error": "something went wrong..."})


@seller_required
def add_new_product(request):
    category = Category.objects.all()
    if request.method == "POST":

        try:
            user = request.user
            name = request.POST.get("name")
            mrp = request.POST.get("mrp")
            model_name = request.POST.get("modelname")
            brand = request.POST.get("brand")
            color = request.POST.get("color")
            price = request.POST.get("price")
            foundcategory = request.POST.get("category")
            tags = request.POST.get("tags")
            features = request.POST.get("features")

            if foundcategory:
                foundcategory = Category.objects.get(name=foundcategory)

            description = request.POST.get("description")
            seller_name = user.seller.name if hasattr(user, "seller") else None
            image1 = request.FILES.get("image1")
            image2 = request.FILES.get("image2")
            image3 = request.FILES.get("image3")
            image4 = request.FILES.get("image4")
            image5 = request.FILES.get("image5")
            p = Product.objects.create(
                name=name,
                price=price,
                mrp=mrp,
                image=image1,
                description=description,
                color=color,
                brand=brand,
                model_name=model_name,
            )
            if tags:
                p.tags = tags
            if features:
                p.special_featuers = features

            if image2:
                p.image2 = image2
            if image3:
                p.image3.save(image3.name, image3)
            if image4:
                p.image4.save(image4.name, image4)
            if image5:
                p.image5.save(image5.name, image5)
            p.category = foundcategory
            p.save()

            return render(request, "add_product.html", {"category": category})
        except Exception as e:
            traceback.print_exc()
            print(e)

    return render(request, "add_product.html", {"category": category})
