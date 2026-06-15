"""
AEM Models

Stores all configurable efficiency factors.

Business Rule:
-------------
No hardcoded factor values inside services.
Everything should come from these database tables so the admin
can modify values without changing code.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# ==========================================================
# Base Model
# ==========================================================

class BaseFactorModel(models.Model):
    """
    Abstract base model for all factor tables.
    """

    factor = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
        ],
        help_text="Efficiency multiplier (0.00 - 1.00)"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


# ==========================================================
# Passenger Factor
# ==========================================================

class PassengerFactor(BaseFactorModel):
    """
    Number of occupants including driver.

    Example

    1 -> 1.00

    2 -> 0.95

    3 -> 0.90
    """

    occupants = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        ordering = ["occupants"]
        verbose_name = "Passenger Factor"
        verbose_name_plural = "Passenger Factors"

    def __str__(self):
        return f"{self.occupants} Occupants → {self.factor}"


# ==========================================================
# Tire Pressure Factor
# ==========================================================

class TirePressureFactor(BaseFactorModel):
    """
    Average tire pressure percentage.
    """

    pressure_percent = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(50),
            MaxValueValidator(100)
        ]
    )

    class Meta:
        ordering = ["-pressure_percent"]
        verbose_name = "Tire Pressure Factor"
        verbose_name_plural = "Tire Pressure Factors"

    def __str__(self):
        return f"{self.pressure_percent}% → {self.factor}"


# ==========================================================
# Vehicle Use Factor
# ==========================================================

class UseFactor(BaseFactorModel):
    """
    Odometer based efficiency degradation.
    """

    odometer_km = models.PositiveIntegerField(
        unique=True
    )

    class Meta:
        ordering = ["odometer_km"]
        verbose_name = "Vehicle Use Factor"
        verbose_name_plural = "Vehicle Use Factors"

    def __str__(self):
        return f"{self.odometer_km:,} km → {self.factor}"


# ==========================================================
# Air Conditioning Factor
# ==========================================================

class ACFactor(BaseFactorModel):
    """
    AC intensity level.

    0 = OFF

    5 = MAX
    """

    ac_level = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        ordering = ["ac_level"]
        verbose_name = "AC Factor"
        verbose_name_plural = "AC Factors"

    def __str__(self):
        return f"Level {self.ac_level} → {self.factor}"


# ==========================================================
# Cargo Load Factor
# ==========================================================

class LoadFactor(BaseFactorModel):
    """
    Vehicle cargo load percentage.
    """

    load_percent = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Meta:
        ordering = ["load_percent"]
        verbose_name = "Load Factor"
        verbose_name_plural = "Load Factors"

    def __str__(self):
        return f"{self.load_percent}% Load → {self.factor}"