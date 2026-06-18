from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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