from drf_spectacular.utils import extend_schema

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers.register import RegisterSerializer, RegisterResponseSerializer


@extend_schema(responses=RegisterResponseSerializer)
class RegisterAPIView(generics.GenericAPIView):
    """
    Register user by email
    """
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(tokens, status=status.HTTP_201_CREATED)
