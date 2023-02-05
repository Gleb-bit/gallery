from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    password = serializers.CharField(write_only=True, max_length=68, min_length=6, required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    def save(self):
        if 'email' in self.validated_data:
            user = User.objects.filter(email=self.validated_data['email']).first()

            if user is None or not user.email_verified:
                raise serializers.ValidationError({'detail': 'Адрес электронной почты '
                                                             'не зарегистрирован в системе. '
                                                             'Пройдите регистрацию для входа'})

        else:
            raise serializers.ValidationError({'detail': 'Должна быть почта'})

        if user.status != User.Status.IN_REGISTRATION:
            raise serializers.ValidationError({'detail': 'Вы уже зарегистрированы'})

        password = self.validated_data.pop('password')
        user.set_password(password)

        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name'] if 'last_name' \
                                                             in self.validated_data else None

        user.is_active = True

        user.status = User.Status.REGISTERED
        user.save()

        return user


class RegisterResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)
    access = serializers.CharField(max_length=255)
