from rest_framework.views import APIView
from .serializers import *
from .services import *
from core.responses import APIResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from .helpers import build_user_response

class SendPhoneOTPView(
    APIView
):

    permission_classes = []

    def post(self, request):

        serializer = SendPhoneOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        OTPService.send_phone_otp(

            serializer.validated_data['phone']
        )

        return APIResponse.success(

            message='OTP sent'
        )

class VerifyPhoneOTPView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = VerifyPhoneOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']

        if otp != "123456":
            return APIResponse.error(
                message="Invalid OTP"
            )

        country_code = serializer.validated_data.get(
            "country_code",
            "US"
        )

        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                "login_provider": "phone",
                "country_code": country_code,
            },
        )

        if not created and not user.country_code:
            user.country_code = country_code
            user.save(update_fields=["country_code"])

        if not user.is_phone_verified:
            user.is_phone_verified = True
            user.save(update_fields=["is_phone_verified"])

        user = sync_subscription_status(user)
        tokens = AuthService.generate_tokens(user)
        
        limits = get_user_entitlements(user)

        return APIResponse.success(
            data={
                "user": build_user_response(user)

                **tokens,
            }
        )

class SendEmailOTPView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = SendEmailOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        OTPService.send_email_otp(
            serializer.validated_data["email"]
        )

        return APIResponse.success(
            message="OTP sent"
        )

class VerifyEmailOTPView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = VerifyEmailOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        if otp != "123456":
            return APIResponse.error(
                message="Invalid OTP"
            )

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                "login_provider": "email",
            },
        )

        if not user.is_email_verified:
            user.is_email_verified = True
            user.save(update_fields=["is_email_verified"])

        user = sync_subscription_status(user)
        tokens = AuthService.generate_tokens(user)

        return APIResponse.success(
            data={
                "user": build_user_response(user)
                **tokens,
            }
        )

class SocialLoginView(
    APIView
):

    permission_classes = []

    def post(self, request):

        serializer = SocialLoginSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        user = AuthService.social_login(
            serializer.validated_data[
                'provider'
            ],

            serializer.validated_data[
                'id_token'
            ],
        )

        user = sync_subscription_status(user)
        tokens = AuthService.generate_tokens(user)

        return APIResponse.success(
            data={
                "user": build_user_response(user)

                **tokens,
            }
        )


class CompleteProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = sync_subscription_status(request.user)

        user.name = request.data.get(
                "name",
                ""
        )

        user.email = request.data.get(
                "email",
                ""
        )

        user.save()

        return APIResponse.success(
            message="Profile updated",
            data={
                "user": build_user_response(user)
            }
        )

class DeleteAccountView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        user = request.user

        user.delete()

        return APIResponse.success(
            message="Account deleted successfully"
        )