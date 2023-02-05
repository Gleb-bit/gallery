import threading

from django.core.mail import EmailMessage

from rest_framework import serializers
from rest_framework.response import Response
from smtplib import SMTPRecipientsRefused

from gallery_and_user import settings


class DefaultSerializer(serializers.Serializer):
    pass


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.email.send()
        except SMTPRecipientsRefused:
            print({"error": "wrong email"})


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']],
            from_email=settings.EMAIL_HOST_USER)
        print(data['email_subject'])
        EmailThread(email).start()


def check_errors(field, serializer, errors, trans_field):
    if field in serializer.errors:
        if serializer.errors[field][0] == f"Пользователь с таким {trans_field} уже существует." or \
                serializer.errors[field][
                    0] == f"Пользователь с таким {trans_field} уже существует.":
            errors[field] = f'{field} exists'
        if serializer.errors[field][0] == \
                "Это поле не может быть пустым.":
            errors[field] = f'blank {field}'
    return errors


def get_data_response(serializer, items, many=True, check_valid=False, status=200):
    # if not items:
    #    return Response({"detail": "Not found."}, status=404)
    if not items:
        return Response([])

    items_serializer = serializer(items, many=many)

    if check_valid:
        items_serializer.is_valid(raise_exception=True)

    return Response(data=items_serializer.data, status=status)
