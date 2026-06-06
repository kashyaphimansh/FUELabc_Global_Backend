from django.urls import path

from .views import (
    SendPhoneOTPView,
    VerifyPhoneOTPView,
    SocialLoginView,
    CompleteProfileView
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

    path(
        'social-login/',
        SocialLoginView.as_view(),
    ),

    path(
        'complete-profile/',
        CompleteProfileView.as_view(),
    ),
]