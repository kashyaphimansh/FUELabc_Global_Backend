from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DrivingProfile
from .serializers import DrivingProfileInputSerializer, DrivingProfileResultSerializer
from .services.mileage_calculator import (
    BEST_SPEED,
    build_speed_mileage_table,
    get_best_speed_savings,
)


def _build_result_payload(profile: DrivingProfile) -> dict:
    """Shared helper: turns a saved DrivingProfile into the full result payload."""
    table, arai = build_speed_mileage_table(
        user_speed=profile.preferred_speed,
        user_mileage=profile.mileage,
        fuel_price=profile.fuel_price,
    )
    cost_at_pref, cost_at_best, savings = get_best_speed_savings(
        user_speed=profile.preferred_speed,
        user_mileage=profile.mileage,
        fuel_price=profile.fuel_price,
    )

    return {
        "fuel_price": profile.fuel_price,
        "preferred_speed": profile.preferred_speed,
        "mileage": profile.mileage,
        "arai_mileage": round(arai, 2),
        "best_speed": BEST_SPEED,
        "cost_at_preferred_speed": cost_at_pref,
        "cost_at_best_speed": cost_at_best,
        "savings_per_unit": savings,
        "table": table,
    }


class DrivingProfileView(APIView):
    """
    POST /api/mileage-advisor/driving-profile/
        Saves (creates or updates) the logged-in user's fuel price,
        preferred speed, and mileage. Returns the computed
        speed (30-120) vs mileage vs cost table.

    GET /api/mileage-advisor/driving-profile/
        Returns the logged-in user's previously saved profile +
        the same computed table, recalculated from stored values.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = DrivingProfileInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        profile, _created = DrivingProfile.objects.update_or_create(
            user=request.user,
            defaults={
                "country": data.get("country", "India"),
                "state_name": data.get("state_name", ""),
                "fuel_type": data.get("fuel_type", "petrol"),
                "fuel_price": data["fuel_price"],
                "preferred_speed": data["preferred_speed"],
                "mileage": data["mileage"],
            },
        )

        result = _build_result_payload(profile)
        output_serializer = DrivingProfileResultSerializer(result)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            profile = request.user.driving_profile
        except DrivingProfile.DoesNotExist:
            return Response(
                {"detail": "No driving profile found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        result = _build_result_payload(profile)
        output_serializer = DrivingProfileResultSerializer(result)
        return Response(output_serializer.data, status=status.HTTP_200_OK)