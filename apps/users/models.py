from django.db import models

from core.models import BaseModel


class User(BaseModel):

    LOGIN_PROVIDER = (

        ('phone', 'Phone'),

        ('email', 'Email'),

        ('google', 'Google'),

        ('apple', 'Apple'),
    )

    phone = models.CharField(

        max_length=20,

        unique=True,

        blank=True,

        default='',
    )

    email = models.EmailField(

        unique=True,

        blank=True,

        default='',
    )

    full_name = models.CharField(

        max_length=255,

        blank=True,

        default='',
    )

    profile_image = models.TextField(

        blank=True,

        default='',
    )

    login_provider = models.CharField(

        max_length=20,

        choices=LOGIN_PROVIDER,
    )

    is_vehicle_setup_done = models.BooleanField(

        default=False,
    )

    def __str__(self):

        return self.full_name