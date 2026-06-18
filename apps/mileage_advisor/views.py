from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DrivingProfile
from .serializers import (
    DrivingProfileInputSerializer,
    DrivingProfileResultSerializer,
)
from .services.country_formatter import (
    format_response,
    KM_TO_MILES,
    KM_L_TO_MPG,
    LITER_TO_GALLON,
)
from .services.mileage_calculator import (
    BEST_SPEED,
    build_speed_mileage_table,
    get_best_speed_savings,
)


def normalize_request(country: str, data: dict):
    """
    Converts USA request values to metric before calculation.

    USA sends:
        Speed      -> mph
        Mileage    -> mpg
        Fuel Price -> $/gallon

    Calculator expects:
        Speed      -> km/h
        Mileage    -> km/l
        Fuel Price -> $/liter
    """
    country = (country or "USA").strip().lower()

    data = data.copy()

    if country == "usa":
        data["fuel_price"] = round(
            data["fuel_price"] / LITER_TO_GALLON,
            4,
        )

        data["preferred_speed"] = round(
            data["preferred_speed"] / KM_TO_MILES,
            4,
        )

        data["mileage"] = round(
            data["mileage"] / KM_L_TO_MPG,
            4,
        )

    return data


def _build_result_payload(profile: DrivingProfile) -> dict:
    """
    Shared helper: turns a saved DrivingProfile into the full result payload.
    """

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

    Saves or updates the user's driving profile and returns
    the calculated mileage response according to country.

    GET /api/mileage-advisor/driving-profile/

    Returns the saved profile and formatted response.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = DrivingProfileInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        request_data = input_serializer.validated_data

        # Default Country = USA
        country = request_data.get("country") or "USA"

        # Convert USA request to metric
        normalized_data = normalize_request(country, request_data)

        profile, _created = DrivingProfile.objects.update_or_create(
            user=request.user,
            defaults={
                "country": country,
                "state_name": normalized_data.get("state_name", ""),
                "fuel_type": normalized_data.get("fuel_type", "petrol"),
                "fuel_price": normalized_data["fuel_price"],
                "preferred_speed": normalized_data["preferred_speed"],
                "mileage": normalized_data["mileage"],
            },
        )

        result = _build_result_payload(profile)

        # Convert response according to country
        result = format_response(country, result)

        output_serializer = DrivingProfileResultSerializer(result)

        return Response(
            output_serializer.data,
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        try:
            profile = request.user.driving_profile
        except DrivingProfile.DoesNotExist:
            return Response(
                {
                    "detail": "No driving profile found for this user."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        result = _build_result_payload(profile)

        # Format according to saved country
        result = format_response(profile.country, result)

        output_serializer = DrivingProfileResultSerializer(result)

        return Response(
            output_serializer.data,
            status=status.HTTP_200_OK,
        )