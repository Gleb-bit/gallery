from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from accounts import services
from accounts.models import User
from gallery_and_user import settings


class RequestEmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()

    @transaction.atomic
    def save(self, **kwargs):
        user, _ = User.objects.get_or_create(email=self.validated_data['email'])

        if user.email_verified and user.status == 1:
            raise serializers.ValidationError({'detail': 'Аккаунт уже подтверждён'})

        code = services.generate_code()
        code_expires = timezone.now() + timezone.timedelta(
            minutes=settings.RECOVER_PASSWORD_CODE_EXPIRES_MINUTES
        )
        user.is_active = False
        user.status = User.Status.IN_REGISTRATION
        user.save()

        services.set_email_verify_code(user, code, code_expires)

        email_body = '    Здравствуйте!\n' \
                     'Для подтверждения адреса электронной почты введите указанный ' \
                     'ниже код в приложении: \n' + str(code)
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Код подтверждения ' + str(code)}
        services.Util.send_email(data)
        return user


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    @transaction.atomic
    def save(self, **kwargs):
        user = User.objects.get(email=self.validated_data['email'])

        is_valid_code = services.verify_code(
            input_code=self.validated_data['code'],
            code=user.temp.email_verify_code,
            code_expires=user.temp.email_verify_code_expires
        )
        if not is_valid_code:
            raise serializers.ValidationError({'detail': 'Неверный код, попробуйте ещё раз'})

        user.temp.email_verify_code = None
        user.temp.email_verify_code_expires = None
        user.temp.save()

        user.email_verified = True

        user.save()

        return user


class ChangeEmailSerializer(serializers.Serializer):
    pass


class ChangeEmailConfirmSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    code = serializers.CharField(max_length=8)


class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
