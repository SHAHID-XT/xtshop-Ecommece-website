from django.shortcuts import render
from .models import *


def update_user_visit_count(request):
    page_url = request.path
    exclude = ["media", "admin", ".png", ".jpg", ".js", ".css"]
    for pattern in exclude:
        if pattern in request.path:
            return
    client_ip = request.META.get("REMOTE_ADDR")
    # Check if the IP address already exists in the database
    request_log, created = RequestLog.objects.get_or_create(
        ip_address=client_ip, page_url=page_url
    )

    # If the IP address already exists, increment the visit count
    if not created:
        request_log.visit_count += 1
        request_log.save()


def user_login_log(user, request):
    ip_address = request.META.get("REMOTE_ADDR")
    login_record, created = UserLoginLog.objects.get_or_create(
        user=user, ip_address=ip_address
    )
    if not created:
        login_record.login_count += 1  # Increment login count if record already exists
        login_record.save()
