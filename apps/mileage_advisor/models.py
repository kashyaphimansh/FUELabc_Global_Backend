from django.conf import settings
from django.db import models


class DrivingProfile(models.Model):
    """
    Stores a single user's self-reported driving data:
    fuel price, preferred speed, and the mileage their vehicle
    gives them at that speed. Applies to 4-wheelers only.

    One profile per user (OneToOne) -- matches the frontend flow
    where vehicle setup step 7 overwrites/creates this data for
    the logged-in user.
    """

    COUNTRY_CHOICES = [
        ("India", "India"),
        ("USA", "USA"),
        ("Canada", "Canada"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="driving_profile",
    )

    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES, default="India")
    state_name = models.CharField(max_length=64, blank=True, default="")

    fuel_type = models.CharField(max_length=20, default="petrol")
    fuel_price = models.FloatField(help_text="Price per litre/gallon/kWh, in local currency")

    preferred_speed = models.FloatField(help_text="User's preferred driving speed (km/hr)")
    mileage = models.FloatField(help_text="User-reported mileage (km/l or mpg) at preferred_speed")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Driving Profile"
        verbose_name_plural = "Driving Profiles"

    def __str__(self):
        return f"{self.user} -> {self.preferred_speed} km/hr @ {self.mileage}"