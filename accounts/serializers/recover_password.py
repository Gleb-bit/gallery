import uuid

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from accounts import services
from accounts.models import User
from gallery_and_user import settings


class SendRecoverLetterSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self):
        code = services.generate_code()
        code_expires = timezone.now() + timezone.timedelta(
            minutes=settings.RECOVER_PASSWORD_CODE_EXPIRES_MINUTES
        )

        user = services.set_or_check_code_and_get_data(self.validated_data, set_code=True, code=code,
                                                       code_expires=code_expires).get('user')

        return user


class ConfirmLetterSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    email = serializers.EmailField()

    @transaction.atomic
    def save(self):
        data = services.set_or_check_code_and_get_data(self.validated_data, check_code=True)

        is_valid_code = data.get('is_valid_code')
        user = data.get('user')

        if not is_valid_code:
            raise serializers.ValidationError({'detail': 'Неверный код, попробуйте ещё раз'})

        user.temp.email_verify_code = None
        user.temp.email_verify_code_expires = None

        # set secret ket for password recover
        code_expires = timezone.now() + timezone.timedelta(
            minutes=settings.RECOVER_PASSWORD_CODE_EXPIRES_MINUTES
        )
        user.temp.password_recover_key = uuid.uuid4()
        user.temp.password_recover_key_expires = code_expires
        user.temp.save()
        return user


class ConfirmLetterSerializerForSchema(serializers.Serializer):
    secret = serializers.CharField(max_length=255)


class RecoverPasswordSerializer(serializers.Serializer):
    secret = serializers.UUIDField()
    new_password = serializers.CharField(max_length=100)

    @transaction.atomic
    def save(self, **kwargs):
        secret = self.validated_data['secret']
        new_password = self.validated_data['new_password']
        user = User.objects.get(temp__password_recover_key=secret)

        is_valid_secret = services.verify_code(
            input_code=secret,
            code=user.temp.password_recover_key,
            code_expires=user.temp.password_recover_key_expires
        )

        if not is_valid_secret:
            raise serializers.ValidationError({'detail': 'Неверная строка активации'})

        user.temp.password_recover_key = None
        user.temp.password_recover_key_expires = None
        user.temp.save()
        print('password', user, new_password)
        user.set_password(new_password)
        user.save()
        return user
