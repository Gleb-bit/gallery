from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views.register import RegisterAPIView
from .views.recover_password import RecoverPasswordAPIView, SendRecoverLetterAPIView, ConfirmLetterAPIView
from .views.login import logout_view, UserMeViewSet, LoginView
from .views.email import ChangeEmail, ChangeEmailConfirm, EmailVerifyAPIView, CheckEmail

auth_urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', logout_view, name='logout'),

    path('simple_login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('simple_login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('email/verify/', EmailVerifyAPIView.as_view(), name="email_verify"),

    path('email/change/', ChangeEmail.as_view(), name="email_change"),
    path('email/change/confirm/', ChangeEmailConfirm.as_view(), name="email_change_confirm"),

    path('email/check/<str:email>', CheckEmail.as_view(), name='check_email'),

    path('password/recover-request/', SendRecoverLetterAPIView.as_view(), name='password_recover_request'),
    path('password/recover-key/', ConfirmLetterAPIView.as_view(), name='password_recover_key'),
    path('password/recover/', RecoverPasswordAPIView.as_view(), name='password_recover'),
]

urlpatterns = [
    path('profile/', UserMeViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update'
    }), kwargs={'pk': 'me'}, name='user_me'),

]
