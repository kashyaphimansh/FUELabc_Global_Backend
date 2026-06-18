"""
Country specific response formatter.

Calculator always works internally in:

- km/h
- km/l
- fuel price per litre

This file converts ONLY the response according to country.
"""

KM_TO_MILES = 0.621371
KM_L_TO_MPG = 2.35215
LITER_TO_GALLON = 0.264172


def format_response(country: str, data: dict):
    """
    Convert metric response to country specific format.

    Internal Calculator
    -------------------
    Speed      : km/h
    Mileage    : km/l
    Fuel Price : per litre

    USA
    ----
    Speed      : mph
    Mileage    : mpg
    Fuel Price : $/gallon

    Canada
    -------
    Metric

    India
    -----
    Metric
    """

    country = (country or "USA").strip().lower()

    formatted = dict(data)

    # ===================================================
    # USA
    # ===================================================
    if country == "usa":

        formatted["fuel_price"] = round(
            data["fuel_price"] * LITER_TO_GALLON,
            2,
        )

        formatted["preferred_speed"] = round(
            data["preferred_speed"] * KM_TO_MILES,
            2,
        )

        formatted["best_speed"] = round(
            data["best_speed"] * KM_TO_MILES,
            2,
        )

        formatted["mileage"] = round(
            data["mileage"] * KM_L_TO_MPG,
            2,
        )

        formatted["arai_mileage"] = round(
            data["arai_mileage"] * KM_L_TO_MPG,
            2,
        )

        formatted["cost_at_preferred_speed"] = round(
            data["cost_at_preferred_speed"] / KM_TO_MILES,
            2,
        )

        formatted["cost_at_best_speed"] = round(
            data["cost_at_best_speed"] / KM_TO_MILES,
            2,
        )

        formatted["savings_per_unit"] = round(
            data["savings_per_unit"] / KM_TO_MILES,
            2,
        )

        formatted["table"] = [
            {
                "speed": round(row["speed"] * KM_TO_MILES, 2),
                "mileage": round(row["mileage"] * KM_L_TO_MPG, 2),
                "cost": round(row["cost"] / KM_TO_MILES, 2),
            }
            for row in data["table"]
        ]

        return formatted

    # ===================================================
    # Canada
    # ===================================================
    elif country == "canada":
        return formatted

    # ===================================================
    # India
    # ===================================================
    elif country == "india":
        return formatted

    # ===================================================
    # Default -> USA
    # ===================================================
    return format_response("USA", data)