from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("login/", loginView, name="login"),
    path("signup/", signupView, name="signup"),
    path("logout/", custom_logout, name="logout"),
    path("personal-info/", personal_info, name="personal_info"),
    path("profile/", profile, name="profile"),
    path("address/", address_view, name="address"),
    path("change-password/", change_password_view, name="change-password"),
    path("support-ticket/", support_view, name="support-ticket"),
    path("support-ticket/<str:ref>/", ticket_detail_view, name="support-ticket"),
    path("new-ticket/", new_ticket_view, name="new_ticket"),
    path("404/", four0four, name="404"),
    path("sell-on-us/", seller_register, name="seller_register"),
    path("forgot-password/", reset_password, name="forgot_password"),
    path("reset-password/", reset_password_token, name="reset_password_token"),

]
