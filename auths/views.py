from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomUserManager
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from analytics.views import *
from django.contrib.auth.hashers import make_password
from ecommerce.context_processors import global_variables


def custom_logout(request):
    logout(request)
    return custom_redirct(request)


def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not request.POST.get("checkbox") == "on":
            error_message = "Invalid username or password."
            return render(request, "login.html", {"error_message": error_message})
        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # User is authenticated, log them in
            user_login_log(user, request)
            login(request, user)
            # Redirect to a success page, or wherever you want
            return custom_redirct(request)
        else:
            # Authentication failed, display an error message
            error_message = "Invalid username or password."
            return render(request, "login.html", {"error_message": error_message})

    return render(request, "login.html")


def signupView(request):

    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        if password != cpassword:
            # Passwords do not match, handle error
            error_message = "Passwords do not match."
            return render(request, "signup.html", {"error_message": error_message})

        # Create a custom user instance and save it
        user = CustomUser.objects.create_user(
            username=username, email=email, password=password, first_name=name
        )
        login(request, user)

        # Redirect
        return custom_redirct(request)
    else:
        form = CustomUserManager()
    return render(request, "signup.html", {"form": form})


@login_required(login_url="/login")
def personal_info(request):

    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = request.user
        email_already_exits = False
        username_already_exits = False
        foundusername = False
        founduser = False
        try:
            founduser = CustomUser.objects.get(email=email)
            if founduser:
                email_already_exits = founduser
        except:
            pass

        try:
            foundusername = CustomUser.objects.get(username=username)
            if foundusername:
                username_already_exits = founduser
        except:
            pass

        if foundusername and foundusername.username == request.user.username:
            username_already_exits = False

        if founduser and founduser.email == request.user.email:
            email_already_exits = False

        if email_already_exits:
            error = f"User Already Exits with : {email}"
            return render(request, "personal_info.html", {"error": error})

        if username_already_exits:
            error = f"User Already Exits with : {username}"
            return render(request, "personal_info.html", {"error": error})

        if CustomUser.check_password(user, password):
            user.email = email
            user.username = username
            user.save()
            return render(request, "personal_info.html", {"error": "Changes Saved..."})
        else:
            return render(request, "personal_info.html", {"error": "Wrong Password..."})

    return render(
        request,
        "personal_info.html",
    )


def profile(request):

    return render(request, "profile.html")


@login_required(login_url="/login")
def address_view(request):
    address, created = Address.objects.get_or_create(user=request.user)
    if request.method == "POST":
        pass
        address.full_name = request.POST.get("name")
        address.mobile_number = request.POST.get("mobile")
        address.pincode = request.POST.get("pincode")
        address.line1 = request.POST.get("line1")
        address.line2 = request.POST.get("line2")
        address.landmark = request.POST.get("landmark")
        address.city = request.POST.get("city")
        address.state = request.POST.get("state")
        if address.full_name == None or address.full_name  == "None" or address.pincode == None or address.pincode == "None" or address.line1 == "None" or address.line1 ==None or address.city == "None" or address.city == None or address.state == "None" or address.state == None:
            return render(request, "address.html", {"user": request.user, "address": address,"error":"Missing Address..."})
        address.save()
        return custom_redirct(request,"/address?message=Changes Saved...")
        # return render(
        #     request,
        #     "address.html",
        #     {"user": request.user, "address": address, "error": "Changes Saved..."},
        # )

    return render(request, "address.html", {"user": request.user, "address": address})


@login_required(login_url="/login/")
def change_password_view(request):

    if request.method == "POST":
        if not request.POST.get("password") == request.POST.get("confirm_password"):
            return render(
                request,
                "change-password.html",
                {"user": request.user, "error": "Password do not match..."},
            )

        if request.user.check_password(request.POST.get("oldpassword")):
            request.password = make_password(request.POST.get("password"))
            # Save the updated user object
            request.user.save()
            return redirect("/profile?message=Password Changed...")
        else:
            return render(
                request,
                "change-password.html",
                {"user": request.user, "error": "Something Went Wrong..."},
            )

    return render(request, "change-password.html", {"user": request.user})


@login_required(login_url="/login/")
def support_view(request):
    tickets = SupportTicket.objects.filter(user=request.user)
    return render(request, "support.html", {"tickets": list(tickets)})


@login_required(login_url="/login/")
def new_ticket_view(request):
    PRIORITY_CHOICES = [i[0] for i in SupportTicket.PRIORITY_CHOICES]
    if request.method == "POST":
        text = request.POST.get("text")
        subject = request.POST.get("subject")
        priority = request.POST.get("priority")
        if not text or not subject:
            return render(
                request,
                "new_ticket.html",
                {
                    "PRIORITY_CHOICES": PRIORITY_CHOICES,
                    "error": "Subject or description missing...",
                },
            )

        s = SupportTicket.objects.create(
            user=request.user,
            title=subject,
            priority=priority,
            description=text,
        )
        s.save()
        return redirect(f"/support-ticket/{s.reference_id}")

    return render(
        request,
        "new_ticket.html",
        {
            "PRIORITY_CHOICES": PRIORITY_CHOICES,
        },
    )


@login_required(login_url="/login/")
def ticket_detail_view(request, ref):
    ticket = SupportTicket.objects.filter(user=request.user, reference_id=ref)
    if ticket:
        ticket = ticket[0]
    if not ticket:
        return redirect("/404")
    return render(request, "ticket_detail.html", {"ticket": ticket})


def four0four(request):
    return render(request, "404.html")


@login_required(login_url="/login/")
def seller_register(request):
    seller = None
    if request.method == "POST":
        gstin = request.POST.get("gstin")
        name = request.POST.get("sellername")
        if not gstin and not name:
            return render(
                request,
                "register_seller.html",
                {"error": "Name or GSTIN is missing ...."},
            )
        
        try:
            seller = Seller.objects.get(user=request.user)
        except:
            seller = Seller.objects.create(user=request.user, name=name, gstin=gstin)
        seller.name= name
        seller.gstin = gstin
        seller.save()
        return custom_redirct(request)
    
    try:
        seller = Seller.objects.get(user=request.user)
        if seller and seller.registered:
            return redirect("/?message=Already Registered as seller.")
        else:
            error = "Mandatory verification of seller registration is pending. Please allow up to 24 hours for approval. If 24 hours have already elapsed and your registration is still pending, kindly raise a support ticket for further assistance."
            return render(request, "register_seller.html",{"error":error,"seller":seller})
    except:
        pass

    return render(request, "register_seller.html",{"seller":seller})


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            try:
                created = PasswordResetToken.objects.get(user=user)
                created.delete()
            except:
                pass

            created = PasswordResetToken.objects.create(user=user)
            created.save()
            var = global_variables(request)
            subject = f"Password Reset Instruction for {var['website_name']}"
            protocol = "https" if request.is_secure() else "http"
            reset_url = (
                f"{protocol}://{request.get_host()}/reset-password/?t={created.token}"
            )
            body = f"""
Dear {user.username},
You recently requested to reset your password for your account. Please click on the link below to reset your password. This link will expire in 10 minutes.

Reset Password: {reset_url} 

If you did not request a password reset, please disregard this email.
Thank you,
{var['website_name']} Team.
            """
            try:
                send_email(subject=subject, body=body, to_email=email)
            except:
                pass
        except:
            pass

        return render(request, "password-reset.html", {"info": True, "email": email})

    return render(request, "password-reset.html")


def reset_password_token(request):
    PasswordResetToken.delete_expired_tokens()
    token = request.GET.get("t")
    if not token:
        return render(request, "404.html", {"error": "something went wrong."})
    user_token = None
    try:
        user_token = PasswordResetToken.objects.get(token=token)
    except:
        user_token = None
    if not user_token:
        return render(
            request,
            "password_reset_token.html",
            {
                "user": user_token,
                "error": "Sorry, the password reset link has expired or is invalid. Please request a new one.",
            },
        )

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            return render(
                request,
                "password_reset_token.html",
                {"user": user_token, "error": "password not match..."},
            )
        user = CustomUser.objects.get(id=user_token.user.id)
        user.set_password(password)
        user.save()

        user_token.delete()
        logout(request)
        return custom_redirct(request, "/login/")

    return render(request, "password_reset_token.html", {"user": user_token})
