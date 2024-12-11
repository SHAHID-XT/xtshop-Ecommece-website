from django.http import HttpResponseNotFound


def global_variables(request):
    page_path = request.path
    error2 = False
    try:
        error2 = request.GET.get("message")
    except:
        pass
    isadmin = False
    if request.user.is_authenticated and request.user.is_superuser:
        isadmin = True

    website_name = "Xt Shop"

    current_year = 2024
    ruppes = "₹"
    support_phone="+91 96000 00000"
    support_email="help@support.com"

    return {
        "website_name": website_name,
        "request": request,
        "current_year": current_year,
        "isadmin": isadmin,
        "ruppes": ruppes,
        "page_path": page_path,
        "error2": error2,
        "support_phone":support_phone,
        "support_email":support_email
    }
