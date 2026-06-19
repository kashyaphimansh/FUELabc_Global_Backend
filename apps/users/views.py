from rest_framework.views import APIView
from .serializers import *
from .services import *
from core.responses import APIResponse
from rest_framework.permissions import IsAuthenticated
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

        dial_code = serializer.validated_data.get(
            "dial_code",
            "+1"
        )

        user = User.objects.filter(
            phone=phone
        ).first()

        updated_fields = []

        if not user:

            user = User.objects.create(
                phone=phone,
                login_provider="phone",
                country_code=country_code,
                dial_code=dial_code,
                is_phone_verified=True,
            )

        else:

            if not user.country_code:
                user.country_code = country_code
                updated_fields.append("country_code")

            if not user.dial_code:
                user.dial_code = dial_code
                updated_fields.append("dial_code")

            if not user.is_phone_verified:
                user.is_phone_verified = True
                updated_fields.append("is_phone_verified")

            if updated_fields:
                user.save(update_fields=updated_fields)

        user = sync_subscription_status(user)
        tokens = AuthService.generate_tokens(user)
        
        return APIResponse.success(
            data={
                "user": build_user_response(user),

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

        email = serializer.validated_data["email"].lower().strip()
        otp = serializer.validated_data["otp"]

        if otp != "123456":
            return APIResponse.error(
                message="Invalid OTP"
            )

        user = User.objects.filter(
            email=email
        ).first()

        if not user:
            user = User.objects.create(
                email=email,
                login_provider="email",
                is_email_verified=True,
            )
        else:
            if not user.is_email_verified:
                user.is_email_verified = True
                user.save(update_fields=["is_email_verified"])

        user = sync_subscription_status(user)
        tokens = AuthService.generate_tokens(user)

        return APIResponse.success(
            data={
                "user": build_user_response(user),

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
            serializer.validated_data['provider'],
            serializer.validated_data['id_token'],
        )

        user = sync_subscription_status(user)

        tokens = AuthService.generate_tokens(user)

        return APIResponse.success(
            data={
                "user": build_user_response(user),
                **tokens,
            }
        )

class SendPhoneVerificationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        if not user.phone:
            return APIResponse.error(
                message="Phone number not found"
            )

        OTPService.send_phone_otp(user.phone)

        return APIResponse.success(
            message="OTP sent for phone verification"
        )

class VerifyPhoneVerificationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        otp = request.data.get("otp")

        if otp != "123456":
            return APIResponse.error(
                message="Invalid OTP"
            )

        user = request.user

        user.is_phone_verified = True

        user.save(
            update_fields=[
                "is_phone_verified",
            ]
        )

        return APIResponse.success(
            message="Phone verified",
            data={
                "user": build_user_response(user)
            }
        )

class SendEmailVerificationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        if not user.email:
            return APIResponse.error(
                message="Email not found"
            )

        OTPService.send_email_otp(user.email)

        return APIResponse.success(
            message="OTP sent for email verification"
        )

class VerifyEmailVerificationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        otp = request.data.get("otp")

        if otp != "123456":
            return APIResponse.error(
                message="Invalid OTP"
            )

        user = request.user

        user.is_email_verified = True

        user.save(
            update_fields=[
                "is_email_verified",
            ]
        )

        return APIResponse.success(
            message="Email verified",
            data={
                "user": build_user_response(user)
            }
        )

class CompleteProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = sync_subscription_status(request.user)

        name = request.data.get(
            "name",
            ""
        ).strip()

        email = request.data.get(
            "email",
            ""
        ).lower().strip()

        phone = request.data.get(
            "phone",
            ""
        ).strip()

        # Required validations

        if not name:
            return APIResponse.error(
                message="Name is required"
            )

        if user.login_provider == "phone":

            if not email and not user.email:
                return APIResponse.error(
                    message="Email is required"
                )

        if user.login_provider == "email":

            if not phone and not user.phone:
                return APIResponse.error(
                    message="Phone number is required"
                )

        # Duplicate email check
        if email:

            existing_email = User.objects.filter(
                email=email
            ).exclude(
                id=user.id
            ).exists()

            if existing_email:
                return APIResponse.error(
                    message="Email already linked with another account"
                )

        # Duplicate phone check

        if phone:

            existing_phone = User.objects.filter(
                phone=phone
            ).exclude(
                id=user.id
            ).exists()

            if existing_phone:
                return APIResponse.error(
                    message="Phone already linked with another account"
                )

        # Update user

        user.name = name

        # Email can be set only once
        if not user.email and email:
            user.email = email

        # Phone can be set only once
        if not user.phone and phone:
            user.phone = phone

        # Profile completion

        user.profile_completed = bool(
            user.name and
            user.email and
            user.phone
        )

        user.save()

        return APIResponse.success(
            message="Profile updated",
            data={
                "user": build_user_response(user),
            }
        )

class LogoutView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        user = request.user

        user.current_session_id = None

        user.save(
            update_fields=[
                "current_session_id"
            ]
        )

        return APIResponse.success(
            message="Logged out"
        )

class DeleteAccountView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        user = request.user

        user.delete()

        return APIResponse.success(
            message="Account deleted successfully"
        )