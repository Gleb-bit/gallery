from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from accounts.serializers.recover_password import (
    SendRecoverLetterSerializer,
    ConfirmLetterSerializer,
    RecoverPasswordSerializer, ConfirmLetterSerializerForSchema
)


@extend_schema(tags=['password'])
class SendRecoverLetterAPIView(generics.GenericAPIView):
    """Отправить письмо для восстановления аккаунта"""

    permission_classes = (permissions.AllowAny,)
    serializer_class = SendRecoverLetterSerializer
    throttle_scope = 'password_recover_request'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


@extend_schema(responses=ConfirmLetterSerializerForSchema, tags=['password'])
class ConfirmLetterAPIView(generics.GenericAPIView):
    """Подтвердить письмо для восстановления аккаунта"""

    permission_classes = (permissions.AllowAny,)
    serializer_class = ConfirmLetterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"secret": user.temp.password_recover_key}, status=status.HTTP_200_OK)


@extend_schema(tags=['password'])
class RecoverPasswordAPIView(generics.GenericAPIView):
    """Восстановить пароль"""

    permission_classes = (permissions.AllowAny,)
    serializer_class = RecoverPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
