from .ev_factor_table import get_factor_at_speed

GRAPH_SPEEDS = [50, 60, 70, 80, 90, 100, 110, 120]


def calculate_real_world_range(claimed_range, speed):
    factor = get_factor_at_speed(speed)
    return round(claimed_range * factor, 2)


def calculate_cost_per_km(
    battery_capacity,
    charging_price,
    real_world_range,
):
    if battery_capacity is None:
        return 0.0

    if charging_price is None:
        return 0.0

    if real_world_range is None or real_world_range <= 0:
        return 0.0

    return round(
        (battery_capacity * charging_price)
        / real_world_range,
        2,
    )


def calculate_energy_consumption(
    battery_capacity,
    real_world_range,
):
    if battery_capacity is None:
        return 0.0

    if real_world_range is None or real_world_range <= 0:
        return 0.0

    return round(
        (battery_capacity * 1000)
        / real_world_range,
        2,
    )


def build_ev_speed_table(
    battery_capacity,
    claimed_range,
    charging_price,
):
    table = []

    for speed in GRAPH_SPEEDS:

        real_range = calculate_real_world_range(
            claimed_range,
            speed,
        )

        cost = calculate_cost_per_km(
            battery_capacity,
            charging_price,
            real_range,
        )

        energy = calculate_energy_consumption(
            battery_capacity,
            real_range,
        )

        table.append(
            {
                "speed": speed,
                "range": real_range,
                "cost": cost,
                "energy_consumption": energy,
            }
        )

    return table


def get_best_ev_speed(
    battery_capacity,
    claimed_range,
    charging_price,
):
    table = build_ev_speed_table(
        battery_capacity,
        claimed_range,
        charging_price,
    )

    best = min(
        table,
        key=lambda x: x["cost"],
    )

    return (
        best["speed"],
        best["cost"],
    )