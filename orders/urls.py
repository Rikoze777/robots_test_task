from orders.views import create_order
from django.urls import path

app_name = "orders"

urlpatterns = [
    path('', create_order, name='create_order'),
]
