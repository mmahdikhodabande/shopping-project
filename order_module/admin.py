from django.contrib import admin

# Register your models here.
from order_module.models import Order, Order_details

admin.site.register(Order)
admin.site.register(Order_details)
