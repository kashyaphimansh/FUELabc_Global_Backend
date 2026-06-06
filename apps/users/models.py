from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

class User(AbstractBaseUser, PermissionsMixin):

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

    full_name = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    login_provider = models.CharField(
        max_length=20,
        default="phone",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []