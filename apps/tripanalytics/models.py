"""
Trip Analytics Models
"""

from django.db import models
from django.conf import settings


# ==========================================================
# Trip
# ==========================================================

class Trip(models.Model):

    TRIP_TYPE_CHOICES = [
        ("car", "Car"),
        ("cycle", "Cycle"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trips",
    )

    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trips",
    )

    is_cycle = models.BooleanField(default=False)

    trip_type = models.CharField(
        max_length=20,
        choices=TRIP_TYPE_CHOICES,
        default="car",
    )

    start_time = models.DateTimeField(null=True, blank=True)
    end_time   = models.DateTimeField(null=True, blank=True)

    distance = models.FloatField(default=0.0)

    average_mileage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    co2_emission = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    start_location  = models.CharField(max_length=500, blank=True, default="")
    destination     = models.CharField(max_length=500, blank=True, default="")

    country_code = models.CharField(max_length=5, default="IN")
    is_ended     = models.BooleanField(default=False)
    is_archieved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_time"]
        verbose_name = "Trip"
        verbose_name_plural = "Trips"

    def __str__(self):
        return f"Trip #{self.id} — {self.user}"


# ==========================================================
# Trip Data (speed samples per trip)
# ==========================================================

class TripData(models.Model):

    trip  = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="trip_data",
    )

    speed = models.FloatField(default=0.0)
    time  = models.FloatField(default=0.0)  # seconds from trip start

    class Meta:
        ordering = ["time"]
        verbose_name = "Trip Data"
        verbose_name_plural = "Trip Data"

    def __str__(self):
        return f"TripData trip={self.trip_id} speed={self.speed}"