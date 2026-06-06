from rest_framework.views import APIView

from .serializers import *

from .services import *

from core.responses import APIResponse

from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import AccessToken

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


# class VerifyPhoneOTPView(
#     APIView
# ):

#     permission_classes = []

#     def post(self, request):

#         serializer = VerifyPhoneOTPSerializer(data=request.data)

#         serializer.is_valid(
#             raise_exception=True
#         )

#         phone = serializer.validated_data['phone']

#         user, _ = User.objects.get_or_create(

#             phone=phone,

#             defaults={

#                 'login_provider':
#                     'phone',
#             },
#         )

#         tokens = AuthService.generate_tokens(user)

#         return APIResponse.success(

#             data={

#                 'user': {

#                     'id':
#                         str(user.id),

#                     'phone':
#                         user.phone,
#                 },

#                 **tokens,
#             }
#         )

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

        user, _ = User.objects.get_or_create(
            phone=phone,
            defaults={
                "login_provider": "phone",
            },
        )

        tokens = AuthService.generate_tokens(user)

        return APIResponse.success(
            data={
                "user": {
                    "id": str(user.id),
                    "phone": user.phone,
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


class CompleteProfileView(APIView):

    permission_classes = []

    def post(self, request):

        token = request.headers.get("Authorization").split(" ")[1]

        payload = AccessToken(token)

        user_id = payload["user_id"]

        user = User.objects.get(id=user_id)

        user.full_name = request.data.get("full_name", "")
        user.email = request.data.get("email", "")
        user.save()

        return APIResponse.success(
            message="Profile updated",
            data={
                "id": str(user.id),
                "phone": user.phone,
                "full_name": user.full_name,
                "email": user.email,
            }
        )