"""
Response Formatter

Converts internal metric calculations into
country-appropriate API response.

Calculation logic NEVER changes.
Only response format changes.
"""

from .unit_converter import (
    km_to_miles,
    liters_to_gallons,
    kmpl_to_mpg,
)


def format_efficiency_response(
    result,
    country_code="IN",
):
    """
    Convert efficiency calculator output
    into country-appropriate API response format.

    country_code:
        IN  → km/L  (default)
        AU  → L/100km
        NZ  → L/100km
    """

    # Country-specific fuel economy unit
    use_l100km = country_code in ("AU", "NZ")

    formatted_rows = []

    for row in result["efficiency_table"]:

        kmpl = row["effective_mileage_kmpl"]
        l100km = round(100 / kmpl, 2) if kmpl > 0 else 0

        formatted_rows.append({

            "speed": {
                "kmh": row["speed_kmh"],
                "mph": round(km_to_miles(row["speed_kmh"]), 1),
            },

            "fuel_efficiency": {
                "km_per_litre": kmpl,
                "l_per_100km": l100km,
                "mpg": round(kmpl_to_mpg(kmpl), 2),
                "display": f"{l100km} L/100km" if use_l100km else f"{kmpl} km/L",
            },

            "range": {
                "km": row["range"]["km"],
                "miles": row["range"]["miles"],
            },

            "fuel_required": {
                "litres": row["fuel_required"]["litres"],
                "gallons": row["fuel_required"]["gallons"],
            },

            "cost": {
                "cpk": row["cost"]["cpk"],
                "cost_per_mile": row["cost"]["cpm"],
                "trip_cost": row["cost"]["trip_cost"],
            },

            "fuel_volume": {
                "ml_per_km": row["fuel_volume_ml_per_km"],
            },

            "trip_possible": row["can_complete_trip"],
        })

    optimal = result["optimal_speed"]
    summary = result["summary"]

    opt_kmpl = optimal["effective_mileage_kmpl"]
    opt_l100km = round(100 / opt_kmpl, 2) if opt_kmpl > 0 else 0

    return {

        "country_code": country_code,

        "optimal_speed": {
            "kmh": optimal["speed_kmh"],
            "mph": round(km_to_miles(optimal["speed_kmh"]), 1),
            "reason": optimal["reason"],

            "fuel_efficiency": {
                "km_per_litre": opt_kmpl,
                "l_per_100km": opt_l100km,
                "mpg": round(kmpl_to_mpg(opt_kmpl), 2),
                "display": f"{opt_l100km} L/100km" if use_l100km else f"{opt_kmpl} km/L",
            },
        },

        "summary": {

            "trip_distance": {
                "km": summary["trip_distance"]["km"],
                "miles": summary["trip_distance"]["miles"],
            },

            "current_fuel": {
                "litres": summary["fuel_available"]["litres"],
                "gallons": summary["fuel_available"]["gallons"],
            },

            "fuel_price_per_litre": summary["fuel_price_per_litre"],

            "net_factor": summary["net_factor"],

            "best_case": summary["best_case"],
            "worst_case": summary["worst_case"],

            "speeds_that_can_complete_trip":
                summary["available_speeds"],
        },

        "efficiency_table": formatted_rows,
    }