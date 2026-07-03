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

    ev_price_unit = models.CharField(
        max_length=20,
        default="kWh"
    )

    ev_efficiency_unit = models.CharField(
        max_length=20,
        default="km/kWh"
    )

    fuel_price_min = models.FloatField(default=0)
    fuel_price_max = models.FloatField(default=200)

    ev_price_min = models.FloatField(default=0)
    ev_price_max = models.FloatField(default=50)

    fuel_efficiency_min = models.FloatField(default=1)
    fuel_efficiency_max = models.FloatField(default=100)

    ev_efficiency_min = models.FloatField(default=2)
    ev_efficiency_max = models.FloatField(default=12)

    speed_min = models.FloatField(default=10)
    speed_max = models.FloatField(default=200)

    yearly_distance_min = models.IntegerField(default=1000)
    yearly_distance_max = models.IntegerField(default=100000)

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