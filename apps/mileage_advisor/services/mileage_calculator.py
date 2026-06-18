"""
Core mileage/speed/cost calculation logic.

Ported from the React frontend's:
  - computeARAI(userSpeed, userMileage)
  - getMileageFromARAI(speed, arai)
  - graphData generation (speed loop 30 -> 120, mileage + cost per speed)

How it works:
1. The user gives us ONE real data point: "at my preferred speed X,
   my car gives me Y mileage."
2. We back-calculate the vehicle's baseline ARAI mileage using the
   factor at that speed:
        ARAI = userMileage / (0.9 * factor_at_userSpeed)
3. Using that ARAI baseline, we forward-calculate predicted mileage
   at every speed from 30 to 120:
        mileage_at_speed = ARAI * 0.9 * factor_at_speed
4. Cost per km/mile at each speed = fuel_price / mileage_at_speed
"""

from .factor_table import get_factor_at_speed

GRAPH_SPEEDS = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
BEST_SPEED = 50  # speed at which mileage factor peaks


def compute_arai(user_speed: float, user_mileage: float) -> float:
    """
    Back-calculate the vehicle's baseline ARAI mileage from the
    user's reported speed + mileage data point.
    """
    factor = get_factor_at_speed(user_speed)
    if factor <= 0 or user_mileage <= 0:
        return 0.0
    return user_mileage / (0.9 * factor)


def get_mileage_from_arai(speed: float, arai: float) -> float:
    """
    Forward-calculate predicted mileage at a given speed, using the
    vehicle's ARAI baseline.
    """
    if arai <= 0:
        return 0.0
    value = arai * 0.9 * get_factor_at_speed(speed)
    return max(0.1, round(value, 2))


def build_speed_mileage_table(user_speed: float, user_mileage: float, fuel_price: float):
    """
    Builds the full speed -> mileage -> cost table for speeds 30
    through 120 (in steps of 10), based on a single user-reported
    (speed, mileage) data point and the local fuel price.

    Returns (table, arai) where table is a list of dicts:
        [{"speed": 30, "mileage": 23.4, "cost": 3.74}, ...]
    """
    arai = compute_arai(user_speed, user_mileage)

    table = []
    for speed in GRAPH_SPEEDS:
        mileage = get_mileage_from_arai(speed, arai) if arai > 0 else 0.0
        cost = round(fuel_price / mileage, 2) if mileage > 0 else 0.0
        table.append({
            "speed": speed,
            "mileage": mileage,
            "cost": cost,
        })

    return table, arai


def get_best_speed_savings(user_speed: float, user_mileage: float, fuel_price: float):
    """
    Returns (cost_at_user_speed, cost_at_best_speed, savings_per_unit_distance).
    """
    arai = compute_arai(user_speed, user_mileage)

    mileage_at_user_speed = get_mileage_from_arai(user_speed, arai) if arai > 0 else 0.0
    cost_at_user_speed = round(fuel_price / mileage_at_user_speed, 2) if mileage_at_user_speed > 0 else 0.0

    mileage_at_best_speed = get_mileage_from_arai(BEST_SPEED, arai) if arai > 0 else 0.0
    cost_at_best_speed = round(fuel_price / mileage_at_best_speed, 2) if mileage_at_best_speed > 0 else 0.0

    savings = round(max(0.0, cost_at_user_speed - cost_at_best_speed), 2)

    return cost_at_user_speed, cost_at_best_speed, savings