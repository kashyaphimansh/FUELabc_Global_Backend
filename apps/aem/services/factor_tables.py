"""
Factor Table Service

Responsible for fetching factor values from the database.

This file DOES NOT perform any calculations.

Responsibilities:
-----------------
- Passenger Factor lookup
- Tire Pressure Factor lookup
- Vehicle Use Factor lookup
- AC Factor lookup
- Load Factor lookup
"""

import logging

from apps.aem.models import (
    PassengerFactor,
    TirePressureFactor,
    UseFactor,
    ACFactor,
    LoadFactor,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Utilities
# ==========================================================

def round_to_nearest(value: int, step: int) -> int:
    """
    Round value to nearest step.

    Example

    step=10

    83 -> 80

    87 -> 90

    Python uses banker's rounding:
    85 -> 80
    """

    return round(value / step) * step


# ==========================================================
# Passenger Factor
# ==========================================================

def get_passenger_factor(occupants: int) -> dict:
    """
    Lookup Passenger Factor.
    """

    try:

        row = PassengerFactor.objects.get(
            occupants=occupants
        )

        return {
            "input": occupants,
            "value": row.factor,
            "label": (
                "Driver Only"
                if occupants == 1
                else f"Driver + {occupants - 1} Passenger(s)"
            )
        }

    except PassengerFactor.DoesNotExist:

        logger.warning(
            "PassengerFactor missing for occupants=%s",
            occupants,
        )

        return {
            "input": occupants,
            "value": 1.0,
            "label": "Default Passenger Factor",
        }


# ==========================================================
# Tire Pressure Factor
# ==========================================================

def get_tire_pressure_factor(pressure_percent: int) -> dict:
    """
    Tire pressure lookup.

    Example

    83 -> 80

    87 -> 90
    """

    rounded = round_to_nearest(
        pressure_percent,
        10,
    )

    rounded = max(
        50,
        min(
            100,
            rounded,
        ),
    )

    try:

        row = TirePressureFactor.objects.get(
            pressure_percent=rounded
        )

        return {
            "input": pressure_percent,
            "rounded": rounded,
            "value": row.factor,
            "label": f"{pressure_percent}% Average Tire Pressure",
        }

    except TirePressureFactor.DoesNotExist:

        logger.warning(
            "TirePressureFactor missing for %s%%",
            rounded,
        )

        return {
            "input": pressure_percent,
            "rounded": rounded,
            "value": 1.0,
            "label": "Default Tire Pressure Factor",
        }


# ==========================================================
# Vehicle Use Factor
# ==========================================================

def get_use_factor(odometer_km: int) -> dict:
    """
    Vehicle age factor.

    Uses linear interpolation.

    Example

    50k -> .96

    75k -> .94

    100k -> .92
    """

    rows = list(

        UseFactor.objects

        .order_by(
            "odometer_km"
        )

        .values_list(
            "odometer_km",
            "factor",
        )

    )

    if not rows:

        return {
            "input": odometer_km,
            "value": 1.0,
            "label": "Default Vehicle Use Factor",
        }

    if odometer_km <= rows[0][0]:

        return {
            "input": odometer_km,
            "value": rows[0][1],
            "label": f"{odometer_km:,} km",
        }

    if odometer_km >= rows[-1][0]:

        return {
            "input": odometer_km,
            "value": rows[-1][1],
            "label": f"{odometer_km:,} km",
        }

    for index in range(len(rows) - 1):

        low_km, low_factor = rows[index]

        high_km, high_factor = rows[index + 1]

        if low_km <= odometer_km <= high_km:

            ratio = (
                (odometer_km - low_km)
                /
                (high_km - low_km)
            )

            factor = round(

                low_factor +

                ratio *

                (high_factor - low_factor),

                2,

            )

            return {

                "input": odometer_km,

                "value": factor,

                "label": f"{odometer_km:,} km",

            }

    return {

        "input": odometer_km,

        "value": 1.0,

        "label": "Default Vehicle Use Factor",

    }


# ==========================================================
# AC Factor
# ==========================================================

def get_ac_factor(level: int) -> dict:

    try:

        row = ACFactor.objects.get(
            ac_level=level
        )

        return {
            "input": level,
            "value": row.factor,
            "label": (
                "AC OFF"
                if level == 0
                else f"AC Level {level}"
            ),
        }

    except ACFactor.DoesNotExist:

        return {
            "input": level,
            "value": 1.0,
            "label": "Default AC Factor",
        }


# ==========================================================
# Load Factor
# ==========================================================

def get_load_factor(load_percent: int) -> dict:

    rounded = round_to_nearest(
        load_percent,
        25,
    )

    rounded = max(
        0,
        min(
            100,
            rounded,
        ),
    )

    try:

        row = LoadFactor.objects.get(
            load_percent=rounded
        )

        return {
            "input": load_percent,
            "rounded": rounded,
            "value": row.factor,
            "label": f"{load_percent}% Cargo Load",
        }

    except LoadFactor.DoesNotExist:

        return {
            "input": load_percent,
            "rounded": rounded,
            "value": 1.0,
            "label": "Default Load Factor",
        }