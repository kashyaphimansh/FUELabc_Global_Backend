from django.db import models
from django.contrib.postgres.fields import ArrayField

class CountryConfig(models.Model):

    country_code = models.CharField(
        max_length=5,
        unique=True
    )

    country_name = models.CharField(
        max_length=100
    )

    currency_code = models.CharField(
        max_length=10
    )

    currency_symbol = models.CharField(
        max_length=10
    )

    distance_unit = models.CharField(
        max_length=20
    )

    fuel_volume_unit = models.CharField(
        max_length=20
    )

    fuel_economy_unit = models.CharField(
        max_length=20
    )

    fuel_types = models.JSONField(
        default=list
    )

    subscription_plans = models.JSONField(
        default=dict
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.country_code} - {self.country_name}"