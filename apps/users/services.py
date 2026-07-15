import random
import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, EmailOTP

class OTPService:

    @staticmethod
    def send_email_otp(email):

        otp = str(random.randint(100000, 999999))
        
        EmailOTP.objects.filter(email=email).delete()

        EmailOTP.objects.update_or_create(
            email=email,
            defaults={
                "otp": otp,
                "is_used": False,
            }
        )

        send_mail(
            subject="Your FUELabc Login Verification Code",
            message=f"""Hello,

                    We received a request to sign in to your FUELabc account.

                    Your One-Time Password (OTP) is:

                    {otp}

                    This OTP is valid for 5 minutes and can only be used once.

                    If you did not request this code, you can safely ignore this email.

                    Thank you,

                    The FUELabc Team
                    """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

class AuthService:

    @staticmethod
    def generate_tokens(user):

        session_id = str(
            uuid.uuid4()
        )

        user.current_session_id = session_id

        user.save(
            update_fields=[
                "current_session_id"
            ]
        )

        refresh = RefreshToken.for_user(user)

        refresh["session_id"] = session_id

        return {
            "access_token":
                str(refresh.access_token),

            "refresh_token":
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

            user = User.objects.filter(
                email=email
            ).first()

            if not user:

                user = User.objects.create(
                    email=email,
                    name=name or "",
                    login_provider="google",
                    is_email_verified=True,
                )

            else:

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

def sync_subscription_status(user):

    if (
        user.is_premium
        and
        user.subscription_expires_at
        and
        user.subscription_expires_at <= timezone.now()
    ):

        user.is_premium = False

        user.subscription_plan = "basic"

        user.subscription_expires_at = None

        user.trips_used = 0

        user.save(
            update_fields=[
                "is_premium",
                "subscription_plan",
                "subscription_expires_at",
                "trips_used",
            ]
        )

    return user