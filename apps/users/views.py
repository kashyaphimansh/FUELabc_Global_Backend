from rest_framework.views import APIView

from .serializers import *

from .services import *

from core.responses import APIResponse


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


class VerifyPhoneOTPView(
    APIView
):

    permission_classes = []

    def post(self, request):

        serializer = VerifyPhoneOTPSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        phone = serializer.validated_data['phone']

        user, _ = User.objects.get_or_create(

            phone=phone,

            defaults={

                'login_provider':
                    'phone',
            },
        )

        tokens = AuthService.generate_tokens(user)

        return APIResponse.success(

            data={

                'user': {

                    'id':
                        str(user.id),

                    'phone':
                        user.phone,
                },

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

        tokens = AuthService.generate_tokens(user)

        return APIResponse.success(

            data={

                'user': {

                    'id':
                        str(user.id),

                    'email':
                        user.email,

                    'full_name':
                        user.full_name,
                },

                **tokens,
            }
        )