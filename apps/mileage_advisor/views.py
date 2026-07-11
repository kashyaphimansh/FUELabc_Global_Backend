from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .services.ev_calculator import (
    build_ev_speed_table,
    get_best_ev_speed,
)
from apps.vehicles.models import Vehicle

from .serializers import DrivingProfileResultSerializer

from .services.country_formatter import (
    format_response,
)

from .services.mileage_calculator import (
    BEST_SPEED,
    build_speed_mileage_table,
    get_best_speed_savings,
)


def build_result_payload(vehicle):

    # ---------------- EV ----------------
    if vehicle.fuel_type.lower() == "electric":

        table = build_ev_speed_table(
            battery_capacity=vehicle.battery_capacity,
            claimed_range=vehicle.average_mileage,
            charging_price=float(vehicle.fuel_price),
        )

        best_speed, best_cost = get_best_ev_speed(
            battery_capacity=vehicle.battery_capacity,
            claimed_range=vehicle.average_mileage,
            charging_price=float(vehicle.fuel_price),
        )

        # Preferred speed ka cost nikaalo
        preferred_cost = next(
            (
                row["cost"]
                for row in table
                if row["speed"] == vehicle.average_speed
            ),
            best_cost,
        )

        # ICE ke same table schema
        formatted_table = [
            {
                "speed": row["speed"],
                "mileage": row["range"],  # EV range -> mileage key
                "cost": row["cost"],
                "energy_consumption": row["energy_consumption"],
            }
            for row in table
        ]

        return {
            "vehicle_id": vehicle.id,
            "fuel_type": vehicle.fuel_type,
            # Same keys as ICE
            "fuel_price": float(vehicle.fuel_price),   # Electricity price
            "preferred_speed": vehicle.average_speed,
            "mileage": vehicle.average_mileage,        # Claimed range
            "arai_mileage": vehicle.average_mileage,   # Claimed range
            "best_speed": best_speed,
            "cost_at_preferred_speed": preferred_cost,
            "cost_at_best_speed": best_cost,
            "savings_per_unit": 0.0,
            # EV specific
            "battery_capacity": vehicle.battery_capacity,
            "table": formatted_table,
        }

    # ---------------- ICE ----------------

    table, arai = build_speed_mileage_table(
        user_speed=vehicle.average_speed,
        user_mileage=vehicle.average_mileage,
        fuel_price=float(vehicle.fuel_price),
    )

    cost_at_pref, cost_at_best, savings = get_best_speed_savings(
        user_speed=vehicle.average_speed,
        user_mileage=vehicle.average_mileage,
        fuel_price=float(vehicle.fuel_price),
    )

    return {
        "vehicle_id": vehicle.id,
        "fuel_type": vehicle.fuel_type,
        "fuel_price": float(vehicle.fuel_price),
        "preferred_speed": vehicle.average_speed,
        "mileage": vehicle.average_mileage,
        "arai_mileage": round(arai, 2),
        "best_speed": BEST_SPEED,
        "cost_at_preferred_speed": cost_at_pref,
        "cost_at_best_speed": cost_at_best,
        "savings_per_unit": savings,
        "table": table,
    } 


class MileageAdvisorView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, vehicle_id):

        try:
            vehicle = Vehicle.objects.get(
                id=vehicle_id,
                user=request.user
            )

        except Vehicle.DoesNotExist:
            return Response(
                {
                    "detail": "Vehicle not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        result = build_result_payload(vehicle)

        result = format_response(
            vehicle.country_name,
            result,
        )

        serializer = DrivingProfileResultSerializer(
            result
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )