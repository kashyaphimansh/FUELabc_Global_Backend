from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    SendPhoneOTPView,
    VerifyPhoneOTPView,
    SocialLoginView,
    CompleteProfileView,
    DeleteAccountView,
    SendEmailOTPView,
    VerifyEmailOTPView,
)

urlpatterns = [

    path(
        'send-phone-otp/',
        SendPhoneOTPView.as_view(),
    ),

    path(
        'verify-phone-otp/',
        VerifyPhoneOTPView.as_view(),
    ),

    path('send-email-otp/',SendEmailOTPView.as_view(),name='send_email_otp'),

    path('verify-email-otp/',VerifyEmailOTPView.as_view(),name='verify_email_otp'),

    path(
        'social-login/',
        SocialLoginView.as_view(),
    ),

    path(
        'refresh-token/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    path(
        'complete-profile/',
        CompleteProfileView.as_view(),
    ),

    path(
        'delete-account/',
        DeleteAccountView.as_view(),
    ),
]