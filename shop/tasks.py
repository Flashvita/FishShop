from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def new_order(pk):
    order = Order.objects.get(id=pk)
    subject = 'Заказ оформлен'
    message = "Дорогой покупатель все оформленно"
    sent_mail = send_mail(subject, message, 'vitalijkulesov975@gmail.com', [order.email])
    return sent_mail


