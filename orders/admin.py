from django.contrib import admin
from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = [
        'customer',
        'robot_serial',
    ]
    list_display = [
        'customer',
        'robot_serial',
    ]
