from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

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

    ev_energy_unit = models.CharField(
        max_length=20,
        default="kWh/100KM"
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


class CustomerSupport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="support_requests"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"