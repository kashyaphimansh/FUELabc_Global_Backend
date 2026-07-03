from django.db import models
from django.conf import settings
from datetime import datetime

class Vehicle(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )

    category = models.CharField(
        max_length=30,
        blank=True,
        default=""
    )

    vehicle_type = models.CharField(max_length=50)

    make = models.CharField(max_length=100)

    model = models.CharField(max_length=100 )

    year = models.CharField(
        max_length=4,
        choices=[(str(year), str(year)) for year in range(1900, datetime.now().year + 1)],
        default=str(datetime.now().year),
    )

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

    state_name = models.CharField(
        max_length=50,
        blank=True
    )

    country_name = models.CharField(
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

class VehicleCatalog(models.Model):

    CATEGORY_CHOICES = [
        ("passenger", "Passenger"),
        ("commercial", "Commercial"),
        ("two_wheeler", "Two Wheeler"),
    ]

    VEHICLE_TYPE_CHOICES = [
        ("hatchback", "Hatchback"),
        ("sedan", "Sedan"),
        ("suv", "SUV"),

        ("pickup", "Pickup"),
        ("mini_truck", "Mini Truck"),
        ("medium_truck", "Medium Truck"),
        ("large_truck", "Large Truck"),
        ("mini_bus", "Mini Bus"),
        ("full_bus", "Full Bus"),

        ("motorcycle", "Motorcycle"),
        ("three_wheeler", "Three Wheeler"),
        ("bicycle", "Bicycle"),
        ("other", "Other"),
    ]

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
    )

    vehicle_type = models.CharField(
        max_length=30,
        choices=VEHICLE_TYPE_CHOICES,
    )

    make = models.CharField(max_length=100)

    model = models.CharField(max_length=100)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_by_admin = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "category",
            "vehicle_type",
            "make",
            "model",
        )

    def __str__(self):
        return f"{self.make} {self.model}"