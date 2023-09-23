from django.contrib import admin
from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = [
        'email',
    ]
    list_display = [
        'email',
    ]
