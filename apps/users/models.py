from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

class User(AbstractBaseUser, PermissionsMixin):

    country_code = models.CharField(
        max_length=5,
        default="US"
    )

    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    login_provider = models.CharField(
        max_length=20,
        default="phone",
    )

    is_phone_verified = models.BooleanField(
        default=False,
    )

    is_email_verified = models.BooleanField(
        default=False,
    )

    is_vehicle_setup_done = models.BooleanField(
        default=False,
    )

    profile_completed = models.BooleanField(
        default=False,
    )

    subscription_plan = models.CharField(
        max_length=20,
        default="basic",
    )

    subscription_expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_premium = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []