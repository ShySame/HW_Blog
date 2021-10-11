from celery import shared_task

from django.core.mail import send_mail


@shared_task
def need_send_mail(subject, from_email, message):
    send_mail(subject, message, from_email, ['admin@mail.com', ])
