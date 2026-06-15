"""
Unit Conversion Service

This module contains all unit conversion utilities used by AEM.

Supported Systems
-----------------
- Metric
- US Imperial
- Canada

No business logic should be added here.
"""

from apps.aem.constants import (
    KM_TO_MILES,
    MILES_TO_KM,
    LITER_TO_US_GALLON,
    US_GALLON_TO_LITER,
    KMPL_TO_MPG,
    MPG_TO_KMPL,
    KMH_TO_MPH,
    MPH_TO_KMH,
)


# ==========================================================
# Distance
# ==========================================================

def km_to_miles(km: float) -> float:
    """Convert kilometers to miles."""
    return round(km * KM_TO_MILES, 2)


def miles_to_km(miles: float) -> float:
    """Convert miles to kilometers."""
    return round(miles * MILES_TO_KM, 2)


# ==========================================================
# Fuel Volume
# ==========================================================

def liters_to_gallons(liters: float) -> float:
    """Convert liters to US gallons."""
    return round(liters * LITER_TO_US_GALLON, 3)


def gallons_to_liters(gallons: float) -> float:
    """Convert US gallons to liters."""
    return round(gallons * US_GALLON_TO_LITER, 3)


# ==========================================================
# Fuel Economy
# ==========================================================

def kmpl_to_mpg(kmpl: float) -> float:
    """
    Convert km/L to MPG (US).
    """
    return round(kmpl * KMPL_TO_MPG, 2)


def mpg_to_kmpl(mpg: float) -> float:
    """
    Convert MPG (US) to km/L.
    """
    return round(mpg * MPG_TO_KMPL, 2)


# ==========================================================
# Speed
# ==========================================================

def kmh_to_mph(speed_kmh: float) -> float:
    """Convert km/h to MPH."""
    return round(speed_kmh * KMH_TO_MPH, 2)


def mph_to_kmh(speed_mph: float) -> float:
    """Convert MPH to km/h."""
    return round(speed_mph * MPH_TO_KMH, 2)


# ==========================================================
# Fuel Cost
# ==========================================================

def cost_per_km_to_cost_per_mile(cost_per_km: float) -> float:
    """
    Convert Cost/KM → Cost/Mile.
    """
    return round(cost_per_km * MILES_TO_KM, 2)


def cost_per_mile_to_cost_per_km(cost_per_mile: float) -> float:
    """
    Convert Cost/Mile → Cost/KM.
    """
    return round(cost_per_mile * KM_TO_MILES, 2)


# ==========================================================
# Vehicle Range
# ==========================================================

def range_km_to_miles(range_km: float) -> float:
    """Vehicle range conversion."""
    return km_to_miles(range_km)


def range_miles_to_km(range_miles: float) -> float:
    """Vehicle range conversion."""
    return miles_to_km(range_miles)


# ==========================================================
# Fuel Consumption
# ==========================================================

def liters_per_100km_to_mpg(l_per_100km: float) -> float:
    """
    Convert L/100km → MPG (US).

    Formula:
        MPG = 235.214 / L/100km
    """

    if l_per_100km <= 0:
        return 0.0

    return round(235.214 / l_per_100km, 2)


def mpg_to_liters_per_100km(mpg: float) -> float:
    """
    Convert MPG → L/100km.
    """

    if mpg <= 0:
        return 0.0

    return round(235.214 / mpg, 2)


# ==========================================================
# Helpers
# ==========================================================

def round_currency(value: float) -> float:
    """
    Round currency values to 2 decimal places.
    """
    return round(value, 2)


def round_distance(value: float) -> float:
    """
    Round distance values.
    """
    return round(value, 2)


def round_fuel(value: float) -> float:
    """
    Round fuel values.
    """
    return round(value, 3)


def round_speed(value: float) -> float:
    """
    Round speed values.
    """
    return round(value, 1)