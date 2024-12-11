from django.contrib import admin
from .models import *

admin.site.site_header = "Shahid-Xt"  # default: "Django Administration"
admin.site.index_title = "Shahid-Xt"  # default: "Site administration".
admin.site.site_title = "Shahid-Xt"


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Rating)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(SupportAttachment)
admin.site.register(SupportTicket)
admin.site.register(Seller)
admin.site.register(PasswordResetToken)
