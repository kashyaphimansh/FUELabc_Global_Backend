"""
Response Formatter

Converts internal metric calculations into
North America (USA / Canada) friendly API response.

Calculation logic NEVER changes.
Only response format changes.
"""

from .unit_converter import (
    km_to_miles,
    liters_to_gallons,
    kmpl_to_mpg,
)


def format_efficiency_response(result):
    """
    Convert efficiency calculator output
    into USA / Canada friendly API response format.
    """

    formatted_rows = []

    for row in result["efficiency_table"]:

        formatted_rows.append({

            "speed": {
                "kmh": row["speed_kmh"],
                "mph": round(km_to_miles(row["speed_kmh"]), 1),
            },

            "fuel_efficiency": {
                "km_per_litre": row["effective_mileage_kmpl"],
                "mpg": round(
                    kmpl_to_mpg(row["effective_mileage_kmpl"]),
                    2,
                ),
            },

            # ==============================
            # FIXED RANGE STRUCTURE
            # ==============================
            "range": {
                "km": row["range"]["km"],
                "miles": row["range"]["miles"],
            },

            # ==============================
            # FIXED FUEL STRUCTURE
            # ==============================
            "fuel_required": {
                "litres": row["fuel_required"]["litres"],
                "gallons": row["fuel_required"]["gallons"],
            },

            # ==============================
            # FIXED COST STRUCTURE
            # ==============================
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

    return {

        "optimal_speed": {
            "kmh": optimal["speed_kmh"],
            "mph": round(km_to_miles(optimal["speed_kmh"]), 1),
            "reason": optimal["reason"],

            "fuel_efficiency": {
                "km_per_litre": optimal["effective_mileage_kmpl"],
                "mpg": round(
                    kmpl_to_mpg(optimal["effective_mileage_kmpl"]),
                    2,
                ),
            },
        },

        # ==============================
        # SUMMARY FIXED
        # ==============================
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