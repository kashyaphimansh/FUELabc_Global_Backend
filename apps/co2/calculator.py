"""
CO2 Emission Calculator
Same logic as existing project — no changes to calculations.
"""

import logging

logger = logging.getLogger(__name__)


def calculate_co2_emission(mileage, fuel_type):
    """
    Calculate CO2 emissions in g/km.

    Emission Factors (ARAI Standards):
        Petrol      : 2.28 kg CO2/liter
        Diesel      : 2.64 kg CO2/liter
        CNG         : 1.88 kg CO2/kg
        Electricity : 0.82 kg CO2/kWh
    """
    try:
        if not mileage or mileage <= 0:
            return None

        fuel_type_lower = str(fuel_type).lower().strip()

        if fuel_type_lower in ['electricity', 'ev', 'electric']:
            electricity_emission_factor = 0.82
            electricity_per_km = 1.0 / mileage
            emissions_kg_per_km = electricity_per_km * electricity_emission_factor
            return round(emissions_kg_per_km * 1000, 2)

        emission_factors = {
            'petrol': 2.28,
            'diesel': 2.64,
            'cng':    1.88,
        }

        if fuel_type_lower not in emission_factors:
            fuel_type_lower = 'petrol'

        emission_factor      = emission_factors[fuel_type_lower]
        fuel_consumed_per_km = 1.0 / mileage
        emissions_kg_per_km  = fuel_consumed_per_km * emission_factor

        return round(emissions_kg_per_km * 1000, 2)

    except Exception as e:
        logger.error(f"Error calculating CO2 emission: {e}", exc_info=True)
        return None


def calculate_co2_saved(actual_emission_gkm, baseline_emission_gkm, distance_km):
    """
    Calculate CO2 saved for a trip.

    Positive = saved (drove better than baseline)
    Negative = extra emitted (drove worse than baseline)
    """
    try:
        if actual_emission_gkm is None or baseline_emission_gkm is None:
            return None
        if distance_km is None or distance_km <= 0:
            return None

        saved_per_km     = baseline_emission_gkm - actual_emission_gkm
        total_saved_grams = saved_per_km * distance_km

        return round(total_saved_grams, 2)

    except Exception as e:
        logger.error(f"Error calculating CO2 saved: {e}", exc_info=True)
        return None