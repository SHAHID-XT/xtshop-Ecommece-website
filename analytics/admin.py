from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(RequestLog)
admin.site.register(UserLoginLog)
admin.site.register(Page)
admin.site.register(UserInteraction)