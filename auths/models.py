from typing import Iterable
from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import *
from django.db.models import Count
from django.db.models import Avg
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import timedelta
from simple_history.models import HistoricalRecords
import uuid
from django.contrib.auth.models import User

CustomUser = User

    
class Seller(models.Model):
    user = models.OneToOneField(
       CustomUser, null=True, blank=False,
        related_name="seller",
        on_delete=models.CASCADE

    )
    
    name = models.CharField(max_length=100, null=False, blank=False)
    gstin = models.CharField(max_length=100, null=False, blank=False)
    registered = models.BooleanField(default=True)
    history = HistoricalRecords()

    
    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="address",
        unique=True,
    )
    full_name = models.CharField(max_length=100, null=True, blank=False,default=" ")
    mobile_number = models.CharField(max_length=20, null=True, blank=False)
    pincode = models.CharField(max_length=10, null=True, blank=False)
    line1 = models.CharField(max_length=100, null=True, blank=False)
    line2 = models.CharField(max_length=100, null=True, blank=False)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=False)
    state = models.CharField(max_length=30, null=True, blank=False)
    country = models.CharField(
        max_length=30, null=False, blank=False, default="India", editable=False
    )

    history = HistoricalRecords()

    def __str__(self):
        return f"Address of {self.user.username}"

    def get_current_address(self):
        return str(
            f"{self.line1}, {self.line2}, {self.landmark}, {self.city} {self.state} - {self.pincode}, {self.country}"
        )


class Profile(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="user",
    )

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="profiles")
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username


# Category Model
class Category(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
    


# Product Model
class Product(models.Model):
    product_id = models.CharField(
        max_length=30, null=True, blank=True, default=generate_product_id
    )
    folder_name = models.CharField(
        max_length=10, null=True, blank=True, default=generate_unique_id
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    brand = models.CharField(max_length=20, null=True, blank=False)
    name = models.CharField(max_length=400, null=True, blank=False)
    model_name = models.CharField(max_length=100, null=True, blank=False)
    color = models.CharField(
        max_length=20, null=True, blank=False, default="Multicolor"
    )
    deliverycharges = models.CharField(max_length=5, default="Free", editable=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    tags = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=False, upload_to=product_image_path)
    image2 = models.ImageField(null=True, blank=True, upload_to=product_image_path)
    image3 = models.ImageField(null=True, blank=True, upload_to=product_image_path)
    image4 = models.ImageField(null=True, blank=True, upload_to=product_image_path)
    image5 = models.ImageField(null=True, blank=True, upload_to=product_image_path)
    image6 = models.ImageField(null=True, blank=True, upload_to=product_image_path)
    num_views = models.IntegerField(null=True, blank=True, default=0)
    special_featuers = models.TextField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords()

    @classmethod
    def get_all_categories(cls, num_categories=5):
        # Get top categories along with their counts
        top_categories_with_counts = (
            cls.objects.values("category__name")
            .annotate(count=Count("category"))
            .order_by("-count")[:num_categories]
        )

        return top_categories_with_counts

    @classmethod
    def get_all_brands(cls, num_brands=5):
        # Get top brands along with their counts
        top_brands_with_counts = (
            cls.objects.values("brand")
            .annotate(count=Count("brand"))
            .order_by("-count")[:num_brands]
        )

        # Create a dictionary to store top brands with counts
        top_brands_with_counts_dict = {
            item["brand"]: item["count"] for item in top_brands_with_counts
        }

        return top_brands_with_counts

    def calculate_discount_percent(self):
        if self.mrp <= 0 or self.price <= 0:
            return 0
        discount_percent = ((self.mrp - self.price) / self.mrp) * 100
        return int(discount_percent)

    @property
    def get_all_ratings(self):
        return self.ratings.all()

    @property
    def average_product_rating(self):
        avg = self.ratings.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        if not avg:
            avg = ""
        return avg

    @classmethod
    def filter_by_average_rating(cls, rating):
        if rating:
            # Filter products by average rating
            products_with_rating = cls.objects.annotate(
                avg_rating=Avg("ratings__rating")
            ).filter(avg_rating=rating)
            return products_with_rating
        else:
            # If no rating is provided, return all products
            return cls.objects.all()

    def __str__(self):
        return self.name

    def get_seller_name(self):
        is_seller = False
        try:
            return self.user.seller.name
        except:
            return self.user


class Rating(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="ratings"
    )

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.PositiveIntegerField()  # Store rating as text
    review = models.TextField(blank=True)  # Optional review text
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Rating {self.rating} for {self.product} by {self.user}"


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItem")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords()

    def get_cart_items(self):
        return [cart_item for cart_item in self.cartitem_set.all()]

    def __str__(self):
        return f"Cart for {self.user.username}"

    def total_price(self):
        total = sum(
            item.product.price * item.quantity for item in self.cartitem_set.all()
        )
        return total

    def total_mrp(self):
        return sum(item.product.mrp * item.quantity for item in self.cartitem_set.all())

    def total_discount(self):
        return int(((self.total_mrp - self.total_price) / self.total_mrp) * 100)


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "Pending", "Pending"
        PROCESSING = "Processing", "Processing"
        COMPLETED = "Delivered", "Delivered"
        CANCELLED = "Cancelled", "Cancelled"

    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(
        default=generate_order_number, null=False, blank=False, max_length=20
    )
    status = models.CharField(
        choices=OrderStatus.choices, default=OrderStatus.PROCESSING, max_length=20
    )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE,default=None,null=True, blank=True, 
    )
    order_promotion_discount = models.CharField(
        max_length=20, null=True, blank=True, 
    )
    expected_deliver_date = models.CharField(max_length=20, null=True, blank=True)
    paypal_id = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    label_generated = models.BooleanField(default=False)
    
    history = HistoricalRecords()
    def time_elapsed(self):
        current_time = timezone.now()
        time_difference = current_time - self.created_at
        days = time_difference.days
        hours = time_difference.seconds // 3600
        minutes = (time_difference.seconds % 3600) // 60

        if days > 0:
            return f"{days} days, {hours} hours"
        elif hours > 0:
            return f"{hours} hours, {minutes} minutes"
        else:
            return f"{minutes} minutes"
        
    def get_order_items(self):
        return OrderItem.objects.filter(order=self)

    def is_more_than_one_items(self):
        item_count = OrderItem.objects.filter(order=self).count()  - 1 
        return item_count if item_count > 1 else False

    def get_first_order(self):
        return OrderItem.objects.filter(order=self).first()

    def order_info(self):
        return "Package was handed to resident"

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
    def get_total_quantity(self):
        return sum([f.quantity for f in list(OrderItem.objects.filter(order=self))])
    def save(self, *args, **kwargs):
        
        self.expected_deliver_date = (datetime.now() + timedelta(days=7)).date()
        try:
            self.order_promotion_discount = sum(
                [f.product.mrp - f.product.price for f in self.get_order_items()]
            )
        except:
            pass
        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orderitems",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class TemporaryTransaction(models.Model):
    transaction_id = models.CharField(
        max_length=100, default=generate_order_number, null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_id = models.CharField(
        max_length=100, default=generate_order_number, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    @classmethod
    def delete_expired_transactions(cls):
        # Calculate the expiration time (e.g., 5 minutes ago)
        expiration_time = timezone.now() - timedelta(minutes=5)

        # Delete expired transactions
        cls.objects.filter(created_at__lt=expiration_time).delete()


class SupportTicket(models.Model):
    title = models.CharField(max_length=100)
    reference_id = models.CharField(
        null=True,
        blank=True,
        default=generate_reference_id,
        max_length=20,
        editable=False,
    )
    # Description of the issue
    description = models.TextField()
    reply = models.TextField(null=True,blank=True,default="")
    # Priority level of the ticket
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Low")

    # Status of the ticket
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")

    # Date and time the ticket was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Date and time the ticket was last updated
    updated_at = models.DateTimeField(auto_now=True)

    # User who submitted the ticket
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    attachments = models.ManyToManyField(
        "SupportAttachment", related_name="support_tickets", blank=True
    )
    history = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=True)

    # Date and time the ticket was last updated
    updated_at = models.DateTimeField(auto_now=True)
    def get_attachments(self):
        return [
            str(c.name).split("/")[-1]
            for c in list([f.file for f in self.attachments.all()])
        ]

    def __str__(self):
        return self.title


class SupportAttachment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    file = models.FileField(upload_to="support_ticket_attachments/")
    history = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    # Date and time the ticket was last updated
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.file.name




class PasswordResetToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @classmethod
    def delete_expired_tokens(cls):
        # Calculate the expiration time (e.g., 10 minutes ago)
        expiration_time = timezone.now() - timedelta(minutes=10)
        # Delete expired tokens
        cls.objects.filter(created_at__lt=expiration_time).delete()
    def __str__(self) -> str:
        return self.user.username