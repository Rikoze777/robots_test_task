from django.contrib import admin
from robots.models import Robot


@admin.register(Robot)
class OrderAdmin(admin.ModelAdmin):
    search_fields = [
        'serial',
        'model',
        'version',
    ]
    list_display = [
        'serial',
        'model',
        'version',
        'created',
    ]
