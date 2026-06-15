import random
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class OTPService:

    @staticmethod
    def generate_otp():

        return str(
            random.randint(
                100000,
                999999,
            )
        )

    @staticmethod
    def send_phone_otp(
        phone,
    ):

        otp = OTPService.generate_otp()

        print(otp)

        return otp

    @staticmethod
    def send_email_otp(
        email,
    ):

        otp = OTPService.generate_otp()

        print(otp)

        return otp


class AuthService:

    @staticmethod
    def generate_tokens(user):

        refresh = RefreshToken.for_user(user)

        return {

            'access_token':
                str(
                    refresh.access_token
                ),

            'refresh_token':
                str(refresh),
        }

    @staticmethod
    def social_login(provider, token):

        if provider == "google":

            user_data = id_token.verify_oauth2_token(
                token,
                requests.Request(),
            )

            email = user_data.get("email")
            name = user_data.get("name")

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "name": name or "",
                    "login_provider": "google",
                    "is_email_verified": True,
                },
            )

            updated = False

            if not user.is_email_verified:
                user.is_email_verified = True
                updated = True

            if not user.name and name:
                user.name = name
                updated = True

            if updated:
                user.save()

            return user