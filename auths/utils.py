import os, random, string
from django.utils.crypto import get_random_string
from django.shortcuts import redirect

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


def generate_unique_id():
    return get_random_string(length=5)


def product_image_path(instance, filename):
    if not instance.folder_name:
        # If the instance is not yet saved to the database,
        # generate a unique ID for the product
        unique_id = generate_unique_id()
    else:
        # If the instance is already saved, use the product's folder_name
        unique_id = instance.folder_name

    folder_name = f"{instance.model_name[:10]}_{unique_id}"
    # Combine the folder name with the filename
    return os.path.join("products", folder_name, filename)


def generate_reference_id():
    return "IN"+"".join(random.choices(string.digits, k=15))

def generate_product_id():
    return str(get_random_string(14)).upper()
def generate_order_number():
    return "OD"+"".join(random.choices(string.digits, k=13))


def custom_redirct(request,redirect_path=False):
    next = None
    try:
        next = request.GET.get("next")
    except:
        pass
    if next:
        return redirect(next)
    elif redirect_path:
        return redirect(redirect_path)
    else:
        return redirect("/")
    
    
    
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    # Email configuration
    sender_email = 'shahidxtshahid@gmail.com'
    sender_password = 'fuxdgparuilwsrzg'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Change this to the appropriate port for your SMTP server

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    # Start a secure SMTP connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login to the SMTP server
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, to_email, message.as_string())

    # Close the SMTP connection
    server.quit()

