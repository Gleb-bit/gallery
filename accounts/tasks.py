from django.conf import settings
from django.core.mail import send_mail

from config.django_celery import app


@app.task(name="send_email_msg")
def send_email_msg(email, subject, msg):
    return send_mail(
        subject=subject,
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )

