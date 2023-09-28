from django.dispatch import receiver
from orders.signals import robot_available_signal
from django.core.mail import send_mail
from orders.models import Order
from environs import Env


env = Env()
env.read_env()


@receiver(robot_available_signal)
def notify_customer(sender, robot_serial, **kwargs):
    try:
        order = Order.objects.get(robot_serial=robot_serial)
        customer_email = order.customer.email
        model, version = order.robot_serial.split('_')
        subject = "Ваш робот в наличии!"
        message = '''Добрый день!
            Недавно вы интересовались нашим роботом модели {}, версии {}. 
            Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'''.format(model, version)
        from_email = env('COMPANY_EMAIL')
        recipient_list = [customer_email]

        send_mail(subject, message, from_email, recipient_list)
    except Order.DoesNotExist:
        pass
