from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("The phone number must be set")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    country_code = models.CharField(
        max_length=5,
        default="US"
    )
    
    dial_code = models.CharField(max_length=10, default="+1")

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

    current_session_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
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

    trips_used = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
