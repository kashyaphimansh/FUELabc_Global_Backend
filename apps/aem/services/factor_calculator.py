"""
Adaptive Efficiency Model (AEM)

Factor Calculator

Calculates Net Factor (NF) from vehicle condition inputs.
Response format matches fuelabc.online API standard.

No hardcoded factor values — everything from DB.
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
# Public Function
# ==========================================================

def calculate_factors(
    passenger_count=1,
    tire_pressure_avg_percent=100,
    odometer_km=0,
    ac_level=0,
    load_percent=0,
):
    """
    Calculate Adaptive Efficiency Net Factor.

    NF = PF × TPF × UF × ACF × LF

    Returns format matching fuelabc.online standard.
    """

    passenger = _lookup_passenger_factor(passenger_count)
    tire      = _lookup_tire_factor(tire_pressure_avg_percent)
    use       = _lookup_use_factor(odometer_km)
    ac        = _lookup_ac_factor(ac_level)
    cargo     = _lookup_load_factor(load_percent)

    net_factor = round(
        passenger["value"]
        * tire["value"]
        * use["value"]
        * ac["value"]
        * cargo["value"],
        2,
    )

    formula = (
        f"NF = PF \u00d7 TPF \u00d7 UF \u00d7 ACF \u00d7 LF = "
        f"{passenger['value']} \u00d7 "
        f"{tire['value']} \u00d7 "
        f"{use['value']} \u00d7 "
        f"{ac['value']} \u00d7 "
        f"{cargo['value']} = "
        f"{net_factor}"
    )

    return {
        "net_factor": net_factor,
        "factors": {
            "passenger_factor": {
                "input": passenger["input"],
                "value": passenger["value"],
                "label": passenger["label"],
            },
            "tire_pressure_factor": {
                "input": tire["input"],
                "value": tire["value"],
                "label": tire["label"],
            },
            "use_factor": {
                "input": use["input"],
                "value": use["value"],
                "label": use["label"],
            },
            "ac_factor": {
                "input": ac["input"],
                "value": ac["value"],
                "label": ac["label"],
            },
            "load_factor": {
                "input": cargo["input"],
                "value": cargo["value"],
                "label": cargo["label"],
            },
        },
        "formula": formula,
    }


# ==========================================================
# Passenger
# ==========================================================

def _lookup_passenger_factor(passenger_count):

    try:
        obj = PassengerFactor.objects.get(occupants=passenger_count)
        factor = obj.factor
    except PassengerFactor.DoesNotExist:
        logger.warning("PassengerFactor missing for occupants=%s", passenger_count)
        factor = 1.0

    if passenger_count == 1:
        label = "Driver only"
    else:
        label = f"Driver + {passenger_count - 1} passenger{'s' if passenger_count > 2 else ''}"

    return {
        "input": passenger_count,
        "value": factor,
        "label": label,
    }


# ==========================================================
# Tire Pressure
# ==========================================================

def _lookup_tire_factor(pressure_percent):

    rounded = _round_to_nearest(pressure_percent, 10)
    rounded = max(50, min(100, rounded))

    try:
        obj = TirePressureFactor.objects.get(pressure_percent=rounded)
        factor = obj.factor
    except TirePressureFactor.DoesNotExist:
        logger.warning("TirePressureFactor missing for %s%%", rounded)
        factor = 1.0

    return {
        "input": pressure_percent,
        "value": factor,
        "label": f"{pressure_percent}% avg tire pressure",
    }


# ==========================================================
# Vehicle Use
# ==========================================================

def _lookup_use_factor(odometer_km):

    rows = list(
        UseFactor.objects
        .order_by("odometer_km")
        .values_list("odometer_km", "factor")
    )

    if not rows:
        return {
            "input": odometer_km,
            "value": 1.0,
            "label": f"{odometer_km:,} km on odometer",
        }

    if odometer_km <= rows[0][0]:
        factor = rows[0][1]
    elif odometer_km >= rows[-1][0]:
        factor = rows[-1][1]
    else:
        factor = 1.0
        for i in range(len(rows) - 1):
            low_km, low_f = rows[i]
            high_km, high_f = rows[i + 1]
            if low_km <= odometer_km <= high_km:
                ratio = (odometer_km - low_km) / (high_km - low_km)
                factor = round(low_f + ratio * (high_f - low_f), 2)
                break

    return {
        "input": odometer_km,
        "value": factor,
        "label": f"{odometer_km:,} km on odometer",
    }


# ==========================================================
# Air Conditioning
# ==========================================================

def _lookup_ac_factor(ac_level):

    try:
        obj = ACFactor.objects.get(ac_level=ac_level)
        factor = obj.factor
    except ACFactor.DoesNotExist:
        logger.warning("ACFactor missing for level=%s", ac_level)
        factor = 1.0

    label = "AC OFF" if ac_level == 0 else f"AC Level {ac_level}"

    return {
        "input": ac_level,
        "value": factor,
        "label": label,
    }


# ==========================================================
# Cargo Load
# ==========================================================

def _lookup_load_factor(load_percent):

    rounded = _round_to_nearest(load_percent, 25)
    rounded = max(0, min(100, rounded))

    try:
        obj = LoadFactor.objects.get(load_percent=rounded)
        factor = obj.factor
    except LoadFactor.DoesNotExist:
        logger.warning("LoadFactor missing for load=%s", rounded)
        factor = 1.0

    return {
        "input": load_percent,
        "value": factor,
        "label": f"{load_percent}% cargo load",
    }


# ==========================================================
# Utility
# ==========================================================

def _round_to_nearest(value, step):
    """Round value to nearest step. E.g. 84 -> 80, 86 -> 90"""
    return round(value / step) * step

# """
# Adaptive Efficiency Model (AEM)

# Factor Calculator

# This service calculates the overall Net Factor (NF)
# based on vehicle condition.

# No API calls.
# Only database lookups.
# """

# import logging

# from apps.aem.models import (
#     PassengerFactor,
#     TirePressureFactor,
#     UseFactor,
#     ACFactor,
#     LoadFactor,
# )

# logger = logging.getLogger(__name__)


# # ==========================================================
# # Public Function
# # ==========================================================

# def calculate_factors(
#     passenger_count=1,
#     tire_pressure_avg_percent=100,
#     odometer_km=0,
#     ac_level=0,
#     load_percent=0,
# ):
#     """
#     Calculate Adaptive Efficiency Net Factor.

#     NF =
#     Passenger
#     × Tire
#     × Vehicle Use
#     × AC
#     × Cargo
#     """

#     passenger = _lookup_passenger_factor(passenger_count)

#     tire = _lookup_tire_factor(
#         tire_pressure_avg_percent
#     )

#     vehicle_use = _lookup_use_factor(
#         odometer_km
#     )

#     ac = _lookup_ac_factor(ac_level)

#     cargo = _lookup_load_factor(load_percent)

#     net_factor = round(

#         passenger["value"]
#         * tire["value"]
#         * vehicle_use["value"]
#         * ac["value"]
#         * cargo["value"],

#         3,
#     )

#     return {

#         "net_factor": net_factor,

#         "formula":

#             f"{passenger['value']} × "
#             f"{tire['value']} × "
#             f"{vehicle_use['value']} × "
#             f"{ac['value']} × "
#             f"{cargo['value']} = "
#             f"{net_factor}",

#         "factors": {

#             "passenger": passenger,

#             "tire_pressure": tire,

#             "vehicle_use": vehicle_use,

#             "air_conditioning": ac,

#             "cargo_load": cargo,
#         },
#     }


# # ==========================================================
# # Passenger
# # ==========================================================

# def _lookup_passenger_factor(passenger):

#     try:

#         obj = PassengerFactor.objects.get(
#             occupants=passenger
#         )

#         return {

#             "input": passenger,

#             "value": obj.factor,

#             "description":

#                 f"{passenger} Occupant(s)",
#         }

#     except PassengerFactor.DoesNotExist:

#         logger.warning(
#             "Passenger factor missing."
#         )

#         return {

#             "input": passenger,

#             "value": 1.0,

#             "description": "Default",
#         }


# # ==========================================================
# # Tire Pressure
# # ==========================================================

# def _lookup_tire_factor(pressure):

#     rounded = _round_to_nearest(
#         pressure,
#         10,
#     )

#     rounded = max(
#         50,
#         min(
#             100,
#             rounded,
#         ),
#     )

#     try:

#         obj = TirePressureFactor.objects.get(
#             pressure_percent=rounded
#         )

#         return {

#             "input": pressure,

#             "rounded": rounded,

#             "value": obj.factor,

#             "description":

#                 f"{rounded}% Tire Pressure",
#         }

#     except TirePressureFactor.DoesNotExist:

#         return {

#             "input": pressure,

#             "rounded": rounded,

#             "value": 1.0,

#             "description": "Default",
#         }


# # ==========================================================
# # Vehicle Usage
# # ==========================================================

# def _lookup_use_factor(odometer):

#     rows = list(

#         UseFactor.objects.order_by(
#             "odometer_km"
#         ).values_list(
#             "odometer_km",
#             "factor",
#         )

#     )

#     if not rows:

#         return {

#             "input": odometer,

#             "value": 1.0,

#             "description": "Default",
#         }

#     if odometer <= rows[0][0]:

#         return {

#             "input": odometer,

#             "value": rows[0][1],

#             "description": "New Vehicle",
#         }

#     if odometer >= rows[-1][0]:

#         return {

#             "input": odometer,

#             "value": rows[-1][1],

#             "description": "High Mileage Vehicle",
#         }

#     for index in range(len(rows) - 1):

#         lower_km, lower_factor = rows[index]

#         upper_km, upper_factor = rows[index + 1]

#         if lower_km <= odometer <= upper_km:

#             ratio = (

#                 (odometer - lower_km)

#                 /

#                 (upper_km - lower_km)

#             )

#             factor = round(

#                 lower_factor +

#                 ratio *

#                 (upper_factor - lower_factor),

#                 3,
#             )

#             return {

#                 "input": odometer,

#                 "value": factor,

#                 "description":

#                     f"{odometer:,} km",
#             }

#     return {

#         "input": odometer,

#         "value": 1.0,

#         "description": "Default",
#     }


# # ==========================================================
# # Air Conditioning
# # ==========================================================

# def _lookup_ac_factor(level):

#     try:

#         obj = ACFactor.objects.get(
#             ac_level=level
#         )

#         return {

#             "input": level,

#             "value": obj.factor,

#             "description":

#                 f"AC Level {level}",
#         }

#     except ACFactor.DoesNotExist:

#         return {

#             "input": level,

#             "value": 1.0,

#             "description": "Default",
#         }


# # ==========================================================
# # Cargo Load
# # ==========================================================

# def _lookup_load_factor(load):

#     rounded = _round_to_nearest(
#         load,
#         25,
#     )

#     rounded = max(
#         0,
#         min(
#             100,
#             rounded,
#         ),
#     )

#     try:

#         obj = LoadFactor.objects.get(
#             load_percent=rounded
#         )

#         return {

#             "input": load,

#             "rounded": rounded,

#             "value": obj.factor,

#             "description":

#                 f"{rounded}% Cargo Load",
#         }

#     except LoadFactor.DoesNotExist:

#         return {

#             "input": load,

#             "rounded": rounded,

#             "value": 1.0,

#             "description": "Default",
#         }


# # ==========================================================
# # Utility
# # ==========================================================

# def _round_to_nearest(value, step):

#     """
#     Example

#     84 -> 80

#     86 -> 90
#     """

#     return round(value / step) * step