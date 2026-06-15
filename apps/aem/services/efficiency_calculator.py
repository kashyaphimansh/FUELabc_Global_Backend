"""
AEM (Adaptive Efficiency Model)

Pure calculation engine.

No database.
No API.
No Django models.

Only business calculations.
"""

from .unit_converter import (
    km_to_miles,
    liters_to_gallons,
    kmpl_to_mpg,
)


def calculate_efficiency_table(
    mileage_data,
    distance_km,
    current_fuel_l,
    fuel_price_per_l,
    net_factor=1.0,
    speed_range=None,
):
    """
    Calculates complete efficiency table.

    Parameters
    ----------
    mileage_data : dict
        {30: 14, 40: 16, 50: 17}

    distance_km : float
    current_fuel_l : float
    fuel_price_per_l : float
    net_factor : float
    speed_range : list[int, int] | None

    Returns
    -------
    dict
    """

    speeds = sorted(mileage_data.keys())

    if speed_range:
        minimum, maximum = speed_range
        speeds = [
            s
            for s in speeds
            if minimum <= s <= maximum
        ]

    table = []

    for speed in speeds:

        row = _calculate_row(
            speed=speed,
            base_mileage=mileage_data[speed],
            distance_km=distance_km,
            current_fuel_l=current_fuel_l,
            fuel_price_per_l=fuel_price_per_l,
            net_factor=net_factor,
        )

        table.append(row)

    optimal = _find_best_speed(table)

    feasible = [
        row
        for row in table
        if row["can_complete_trip"]
    ]

    best_case = max(
        table,
        key=lambda x: x["effective_mileage_kmpl"],
    )

    worst_case = min(
        table,
        key=lambda x: x["effective_mileage_kmpl"],
    )

    summary = {
        "trip_distance": {
            "km": round(distance_km, 2),
            "miles": km_to_miles(distance_km),
        },
        "fuel_available": {
            "litres": round(current_fuel_l, 2),
            "gallons": liters_to_gallons(current_fuel_l),  # BUG FIX: was litres_tcurrent_fuel_l
        },
        "fuel_price_per_litre": fuel_price_per_l,
        "net_factor": net_factor,
        "best_case": best_case,
        "worst_case": worst_case,
        "available_speeds": [
            row["speed_kmh"]
            for row in feasible
        ],
    }

    return {
        "optimal_speed": optimal,
        "summary": summary,
        "efficiency_table": table,
    }


def _calculate_row(
    speed,
    base_mileage,
    distance_km,
    current_fuel_l,
    fuel_price_per_l,
    net_factor,
):
    # BUG FIX: effective was inside round() call — now properly calculated first
    effective = round(base_mileage * net_factor, 2)

    fuel_volume_ml_per_km = round(1000 / effective, 1)

    range_km = round(effective * current_fuel_l, 2)

    fuel_required = round(distance_km / effective, 2)

    can_complete = fuel_required <= current_fuel_l

    cost_per_km = round(fuel_price_per_l / effective, 2)

    cost_per_mile = round(cost_per_km * 1.60934, 2)

    total_cost = round(fuel_required * fuel_price_per_l, 2)

    return {

        "fuel_volume_ml_per_km": fuel_volume_ml_per_km,

        # Speed
        "speed_kmh": speed,
        "speed_mph": round(speed * 0.621371, 2),

        # Mileage
        "base_mileage_kmpl": base_mileage,
        "effective_mileage_kmpl": effective,

        # Range
        "range": {
            "km": range_km,
            "miles": km_to_miles(range_km),
        },

        # Fuel
        "fuel_required": {
            "litres": fuel_required,
            "gallons": liters_to_gallons(fuel_required),
        },

        # Cost
        "cost": {
            "cpk": cost_per_km,
            "cpm": cost_per_mile,
            "trip_cost": total_cost,
        },

        # Status
        "can_complete_trip": can_complete,
    }


def _find_best_speed(table):

    if not table:
        return None

    best = max(
        table,
        key=lambda x: x["effective_mileage_kmpl"],
    )

    return {
        "speed_kmh": best["speed_kmh"],
        "speed_mph": best["speed_mph"],
        "effective_mileage_kmpl": best["effective_mileage_kmpl"],
        "estimated_range": best["range"],
        "reason": (
            "Highest effective fuel economy "
            "after applying Adaptive Efficiency Model."
        ),
    }

# """
# AEM (Adaptive Efficiency Model)

# Pure calculation engine.

# No database.
# No API.
# No Django models.

# Only business calculations.
# """

# from .unit_converter import (
#     km_to_miles,
#     liters_to_gallons,
# )


# def calculate_efficiency_table(
#     mileage_data,
#     distance_km,
#     current_fuel_l,
#     fuel_price_per_l,
#     net_factor=1.0,
#     speed_range=None,
# ):
#     """
#     Calculates complete efficiency table.

#     Parameters
#     ----------
#     mileage_data:
#         {
#             30:14,
#             40:16,
#             50:17
#         }

#     Returns
#     -------
#     dict
#     """

#     speeds = sorted(mileage_data.keys())

#     if speed_range:
#         minimum, maximum = speed_range
#         speeds = [
#             s
#             for s in speeds
#             if minimum <= s <= maximum
#         ]

#     table = []

#     for speed in speeds:

#         row = _calculate_row(
#             speed=speed,
#             base_mileage=mileage_data[speed],
#             distance_km=distance_km,
#             current_fuel_l=current_fuel_l,
#             fuel_price_per_l=fuel_price_per_l,
#             net_factor=net_factor,
#         )

#         table.append(row)

#     optimal = _find_best_speed(table)

#     feasible = [
#         row
#         for row in table
#         if row["can_complete_trip"]
#     ]

#     best_case = max(
#         table,
#         key=lambda x: x["effective_mileage_kmpl"],
#     )

#     worst_case = min(
#         table,
#         key=lambda x: x["effective_mileage_kmpl"],
#     )

#     summary = {
#         "trip_distance": {
#             "km": round(distance_km, 2),
#             "miles": km_to_miles(distance_km),
#         },
#         "fuel_available": {
#             "litres": round(current_fuel_l, 2),
#             "gallons": liters_to_gallons(litres_tcurrent_fuel_l),
#         },
#         "fuel_price_per_litre": fuel_price_per_l,
#         "net_factor": net_factor,
#         "best_case": best_case,
#         "worst_case": worst_case,
#         "available_speeds": [
#             row["speed_kmh"]
#             for row in feasible
#         ],
#     }

#     return {
#         "optimal_speed": optimal,
#         "summary": summary,
#         "efficiency_table": table,
#     }


# def _calculate_row(
#     speed,
#     base_mileage,
#     distance_km,
#     current_fuel_l,
#     fuel_price_per_l,
#     net_factor,
# ):

#     effective = round(
#         base_mileage * net_factor,
#         2,
#         fuel_volume_ml_per_km = round(1000 / effective, 1)
#     )

#     range_km = round(
#         effective * current_fuel_l,
#         2,
#     )

#     fuel_required = round(
#         distance_km / effective,
#         2,
#     )

#     can_complete = fuel_required <= current_fuel_l

#     cost_per_km = round(
#         fuel_price_per_l / effective,
#         2,
#     )

#     cost_per_mile = round(
#         cost_per_km * 1.60934,
#         2,
#     )

#     total_cost = round(
#         fuel_required * fuel_price_per_l,
#         2,
#     )

#     return {

#         "fuel_volume_ml_per_km": fuel_volume_ml_per_km,
#         ##################################################
#         # Speed
#         ##################################################

#         "speed_kmh": speed,
#         "speed_mph": round(speed * 0.621371, 2),

#         ##################################################
#         # Mileage
#         ##################################################

#         "base_mileage_kmpl": base_mileage,
#         "effective_mileage_kmpl": effective,

#         ##################################################
#         # Range
#         ##################################################

#         "range": {
#             "km": range_km,
#             "miles": km_to_miles(range_km),
#         },

#         ##################################################
#         # Fuel
#         ##################################################

#         "fuel_required": {
#             "litres": fuel_required,
#             "gallons": liters_to_gallons(fuel_required),
#         },

#         ##################################################
#         # Cost
#         ##################################################

#         "cost": {

#             # USA/Canada naming

#             "cpk": cost_per_km,
#             "cpm": cost_per_mile,

#             "trip_cost": total_cost,
#         },

#         ##################################################
#         # Status
#         ##################################################

#         "can_complete_trip": can_complete,
#     }


# def _find_best_speed(table):

#     if not table:
#         return None

#     best = max(
#         table,
#         key=lambda x: x["effective_mileage_kmpl"],
#     )

#     return {

#         "speed_kmh": best["speed_kmh"],

#         "speed_mph": best["speed_mph"],

#         "effective_mileage_kmpl": best[
#             "effective_mileage_kmpl"
#         ],

#         "estimated_range": best["range"],

#         "reason": (
#             "Highest effective fuel economy "
#             "after applying Adaptive Efficiency Model."
#         ),
#     }