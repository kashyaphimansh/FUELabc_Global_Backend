"""
Speed -> mileage-factor lookup table.

This is a direct port of FOUR_WHEELER_FACTORS + getFactorAtSpeed()
from the frontend (React) logic. The "factor" represents how a
vehicle's fuel efficiency changes relative to its baseline (ARAI)
mileage as speed changes. It peaks around 50 km/hr and falls off
on either side.

NOTE: this logic applies to 4-wheelers only, as designed.
"""

FOUR_WHEELER_FACTORS = [
    {"speed": 30, "factor": 1.3},
    {"speed": 40, "factor": 1.467741935},
    {"speed": 50, "factor": 1.666666667},
    {"speed": 60, "factor": 1.5},
    {"speed": 70, "factor": 1.333333333},
    {"speed": 80, "factor": 1.166666667},
    {"speed": 90, "factor": 0.9},
    {"speed": 100, "factor": 0.8333333333},
]

MIN_TABLE_SPEED = FOUR_WHEELER_FACTORS[0]["speed"]          # 30
MAX_TABLE_SPEED = FOUR_WHEELER_FACTORS[-1]["speed"]          # 100


def get_factor_at_speed(speed: float) -> float:
    """
    Returns the mileage factor at a given speed.

    - Below 30: clamped to the factor at 30.
    - Between 30 and 100: linearly interpolated between table points.
    - Above 100 (up to 120 and beyond): linearly extrapolated using
      the slope of the last two table points (90 -> 100), same as
      the frontend's getFactorAtSpeed().
    """
    data = FOUR_WHEELER_FACTORS
    s = max(MIN_TABLE_SPEED, speed)

    if s <= data[0]["speed"]:
        return data[0]["factor"]

    if s >= data[-1]["speed"]:
        a, b = data[-2], data[-1]
        slope = (b["factor"] - a["factor"]) / (b["speed"] - a["speed"])
        extrapolated = b["factor"] + slope * (s - b["speed"])
        return max(0.05, extrapolated)

    lo = None
    for point in reversed(data):
        if point["speed"] <= s:
            lo = point
            break

    hi = None
    for point in data:
        if point["speed"] > s:
            hi = point
            break

    t = (s - lo["speed"]) / (hi["speed"] - lo["speed"])
    return lo["factor"] + t * (hi["factor"] - lo["factor"])