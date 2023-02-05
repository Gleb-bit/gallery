from django.contrib.auth import authenticate, login
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status, viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

from ..serializers.user import UserSerializer
from accounts.models import User
from accounts.permissions import IsActivated
from ..serializers.login import LoginSerializer, LoginSerializerResopnse


@extend_schema(responses={
    200: LoginSerializerResopnse,
    401: OpenApiResponse(description=_("Неправильный пароль.")),
    402: OpenApiResponse(description=_("Нет аккаунта с такими данными.")),
    403: OpenApiResponse(description=_("Пользователь не активирован."))
})
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        """
        Авторизация пользователя по почте и паролю
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                refresh = RefreshToken.for_user(user)
                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }

                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Аккаунт не активирован'},
                                status=status.HTTP_403_FORBIDDEN)

        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            return Response({
                'detail': 'Введён неверный пароль'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'detail': 'Адрес электронной почты не зарегистрирован в системе. '
                      'Пройдите регистрацию для входа'
        }, status=status.HTTP_402_PAYMENT_REQUIRED)


class UserMeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsActivated, ]
    serializer_class = UserSerializer

    @extend_schema(summary="4. Получение/редактирование профиля")
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def partial_update(self, request, *args, **kwargs):
        if (request.data.get("email", None)):
            if (request.user.email == request.data["email"]):
                request.data.pop("email")
        return self.update(request, *args, **kwargs, partial=True)


class LogoutAPIView(generics.GenericAPIView):
    """Апи для выхода из аккаунта"""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except (TokenBackendError, TokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="12. Выход",
    responses={
        200: OpenApiResponse(
            description="\t{'detail': 'Успешный выход'}"
        ),
        400: OpenApiResponse(
            description="\t{'error': 'Поле refresh обязательно'}\n\n"
                        "\t{'error': 'Неправильный токен'}"
        )
    }
)
def logout_view(request):
    """
    Заносит refresh токен в чёрный список
    """
    if 'refresh' in request.data:
        refresh_token = request.data["refresh"]
        try:
            token = RefreshToken(refresh_token)
        except TokenError:
            return Response({'error': 'Неправильный токен'},
                            status=status.HTTP_400_BAD_REQUEST)
        token.blacklist()
    else:
        return Response({'error': 'Поле refresh обязательно'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Успешный выход"}, status=status.HTTP_200_OK)


class LogoutAllAPIView(generics.GenericAPIView):
    """Апи для выхода из аккаунта"""
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
