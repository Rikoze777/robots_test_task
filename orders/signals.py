from django.db.models.signals import post_save
from django.dispatch import receiver
from environs import Env
from orders.models import Order
from django.core.mail import send_mail
from robots.models import Robot


env = Env()
env.read_env()


@receiver(post_save, sender=Robot)
def create_order(sender, instance, created, **kwargs):
    if created:
        serial = instance.serial
        try:
            order = Order.objects.get(robot_serial=serial)
        except Order.DoesNotExist:
            order = None
        if order:
            email = order.customer.email
            model = instance.model
            version = instance.version
            subject = 'Появился Ваш робот!'
            message = '''Добрый день!
                    Недавно вы интересовались нашим роботом модели {}, версии {}.
                    Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'''.format(model, version)
            from_email = env('EMAIL_HOST_USER')
            recipient_list = [email]
            result = send_mail(subject, message, from_email, recipient_list)
            if result == 1:
                order.delete()
