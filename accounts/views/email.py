from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status, views, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers.email import ChangeEmailSerializer, ChangeEmailConfirmSerializer, \
    EmailVerifySerializer, RequestEmailVerifySerializer, ResendVerificationCodeSerializer
from accounts.services import generate_code
from gallery_and_user.utils import DefaultSerializer, Util


def send_activation_email(user):
    email_body = "    Здравствуйте!\n" \
                 "Вы зарегистрировались. Для активации учётной записи " \
                 "введите код в приложении:\n" + str(user.code)
    data = {'email_body': email_body, 'to_email': user.email,
            'email_subject': f'Код активации {str(user.code)}'}
    Util.send_email(data)


class CheckEmail(generics.GenericAPIView):
    serializer_class = DefaultSerializer

    def get(self, request, email):
        user = User.objects.filter(email=email).first()

        if user:
            return Response(status=200, data={'email': 'already-in-use'})

        return Response(status=200)


class ChangeEmail(views.APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeEmailSerializer

    @extend_schema(summary="Смена электронной почты")
    def post(self, request):
        request.user.code = generate_code()
        request.user.save()
        email_body = '    Здравствуйте!\n' \
                     'Для смены адреса электронной почты введите указанный ' \
                     'ниже код в приложении: \n' + str(request.user.code)
        data = {'email_body': email_body, 'to_email': request.user.email,
                'email_subject': 'Код подтверждения ' + str(request.user.code)}
        Util.send_email(data)
        return Response({'detail': 'Код подтверждения выслан на почту'},
                        status=status.HTTP_200_OK)


class ChangeEmailConfirm(views.APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeEmailConfirmSerializer

    @extend_schema(
        summary="Подтверждение кода для смены электронной почты",
        responses={
            200: OpenApiResponse(
                description="\t{'detail': 'email changed'}"
            ),
            400: OpenApiResponse(
                description="\t{'error': 'field required'}\n\n"
                            "\t{'error': 'wrong code'}\n\n"
            ),
        }
    )
    def post(self, request):
        if 'code' not in request.data:
            return Response({'error': {'code': 'field required'}},
                            status=status.HTTP_400_BAD_REQUEST)
        verify_code = request.data['code']
        if 'new_email' not in request.data:
            return Response({'error': {'new_email': 'field required'}},
                            status=status.HTTP_400_BAD_REQUEST)

        new_email = request.data['new_email']
        user = self.request.user

        if verify_code == user.code:
            user.email = user.username = new_email
            request.user.is_active = True
            user.save()
            return Response({'detail': 'Адрес изменён'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неверный код, попробуйте ещё раз'},
                            status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['email'])
class EmailVerifyAPIView(generics.GenericAPIView):
    """
    Verify email by mail:
    POST - for send mail with code,
    PUT - for verify email
    """
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RequestEmailVerifySerializer
        elif self.request.method == 'PUT':
            return EmailVerifySerializer

    def get_throttles(self):
        if self.request.method == 'POST':
            self.throttle_scope = 'email_verify_request'
        return super().get_throttles()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
