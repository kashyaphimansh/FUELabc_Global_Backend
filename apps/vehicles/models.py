from django.db import models
from django.conf import settings

class Vehicle(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )

    vehicle_type = models.CharField(max_length=50)

    make = models.CharField(max_length=100)

    model = models.CharField(max_length=100 )

    fuel_type = models.CharField(max_length=50)

    fuel_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    average_mileage = models.FloatField()

    average_speed = models.IntegerField()

    yearly_km = models.IntegerField()

    driving_style = models.CharField(
        max_length=50,
        blank=True
    )

    is_active = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.make} {self.model}"