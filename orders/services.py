from customers.models import Customer
from orders.models import Order
from orders.validators import OrderSchema


def add_order(data):
    OrderSchema(**data)
    serial = data['robot_serial']
    email = data['customer']
    customer, _ = Customer.objects.get_or_create(email=email)
    return customer, serial


def save_order(customer, serial):
    Order.objects.create(customer=customer,
                         robot_serial=serial)


def check_order(customer, serial):
    try:
        existing_order = Order.objects.get(customer=customer,
                                           robot_serial=serial)
    except Order.DoesNotExist as err:
        existing_order = None
    return existing_order
