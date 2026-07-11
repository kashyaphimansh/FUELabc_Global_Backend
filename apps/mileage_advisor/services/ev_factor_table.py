"""
EV Speed -> Range Fall Factor Table

The factor represents how the real-world range changes
with speed.

Real World Range = Claimed Range * Fall Factor
"""

EV_FACTORS = [
    {"speed": 50, "factor": 1.11},
    {"speed": 60, "factor": 1.05},
    {"speed": 70, "factor": 1.00},
    {"speed": 80, "factor": 0.95},
    {"speed": 90, "factor": 0.91},
    {"speed": 100, "factor": 0.87},
    {"speed": 110, "factor": 0.83},
    {"speed": 120, "factor": 0.80},
]

MIN_SPEED = EV_FACTORS[0]["speed"]
MAX_SPEED = EV_FACTORS[-1]["speed"]


def get_factor_at_speed(speed: float) -> float:
    """
    Returns fall factor for a given speed.

    Uses linear interpolation between speeds.
    """

    s = max(MIN_SPEED, min(MAX_SPEED, speed))

    if s <= EV_FACTORS[0]["speed"]:
        return EV_FACTORS[0]["factor"]

    if s >= EV_FACTORS[-1]["speed"]:
        return EV_FACTORS[-1]["factor"]

    lower = None
    upper = None

    for point in EV_FACTORS:
        if point["speed"] <= s:
            lower = point

        if point["speed"] >= s:
            upper = point
            break

    if lower["speed"] == upper["speed"]:
        return lower["factor"]

    ratio = (
        (s - lower["speed"])
        / (upper["speed"] - lower["speed"])
    )

    return lower["factor"] + (
        ratio * (upper["factor"] - lower["factor"])
    )