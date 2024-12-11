from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q, Sum

from auths.models import *


def seller_required(view_func):

    def wrapper(request, *args, **kwargs):
        try:
            seller = request.user.seller.registered
            if seller:
                if not seller:
                    return redirect(
                        "/?message=Manual Seller Verification is Pending. If 24 hours have passed, please raise a support ticket."
                    )
                else:
                    try:
                        return view_func(request, *args, **kwargs)
                    except Exception as e:
                        print(e)
                        return redirect("/?message=Something went wrong...")
        except Exception as e:
            print(e)
            return redirect("/sell-on-us/")

    return wrapper


def return_my_order_info(seller_name, user):
    result = {}
    order_status_list = [
        "Pending",
        "Processing",
        "Delivered",
        "Cancelled",
    ]
    for item in order_status_list:
        order_items = OrderItem.objects.filter(
            Q(order__status=item),
            Q(product__user=user) | Q(product__user__seller__name=seller_name),
        ).order_by("-order__created_at")

        orders_length = len(list(set([item.order for item in order_items])))
        result[item.strip().lower()] = orders_length
        
    order_pending = OrderItem.objects.filter(
            Q(order__label_generated=False),
            Q(product__user=user) | Q(product__user__seller__name=seller_name),
        ).order_by("-order__created_at")

    pending_label = len(list(set([item.order for item in order_pending])))
    
    result["pendinglabels"] = pending_label
    
    return result
