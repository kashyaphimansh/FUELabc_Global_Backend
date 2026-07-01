"""
AEM API Views

Adaptive Efficiency Model

Endpoints:
    POST /api/v1/aem/factors/calculate/
    POST /api/v1/aem/efficiency/calculate/
"""

import logging

from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import (
    EfficiencyRequestSerializer,
    FactorRequestSerializer,
)

from .services.factor_calculator import calculate_factors
from .services.efficiency_calculator import calculate_efficiency_table
from .services.response_formatter import format_efficiency_response
from apps.vehicles.models import Vehicle

from apps.mileage_advisor.services.mileage_calculator import (
    build_speed_mileage_table,
)

from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


# ==========================================================
# Factor Calculator
# POST /api/v1/aem/factors/calculate/
# ==========================================================

class FactorCalculatorAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = FactorRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            print("FACTOR ERRORS =", serializer.errors)

            return Response(
                {
                    "status": "error",
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                    "timestamp": timezone.now(),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = calculate_factors(**serializer.validated_data)

            # Response format matching fuelabc.online standard
            return Response(
                {
                    "status": "success",
                    "timestamp": timezone.now(),
                    "net_factor": result["net_factor"],
                    "factors": result["factors"],
                    "formula": result["formula"],
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.exception(e)
            return Response(
                {
                    "status": "error",
                    "message": "Unable to calculate factors.",
                    "error": str(e),
                    "timestamp": timezone.now(),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================================
# Efficiency Calculator
# POST /api/v1/aem/efficiency/calculate/
# ==========================================================

class EfficiencyCalculatorAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = EfficiencyRequestSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            print("EFFICIENCY ERRORS =", serializer.errors)
            print("REQUEST DATA =", request.data)

            return Response(
                {
                    "status": "error",
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                    "timestamp": timezone.now(),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            vehicle = Vehicle.objects.get(
                id=serializer.validated_data["vehicle_id"],
                user=request.user,
            )

            table, _ = build_speed_mileage_table(
                user_speed=vehicle.average_speed,
                user_mileage=vehicle.average_mileage,
                fuel_price=float(vehicle.fuel_price),
            )

            # print("TABLE =", table)

            # Actual conversion after seeing table structure
            mileage_data = {
                row["speed"]: row["mileage"]
                for row in table
            }
            # print("MILEAGE DATA =", mileage_data)

            speed_range = serializer.validated_data.get("speed_range")

            if speed_range:

                minimum, maximum = speed_range

                if minimum not in mileage_data:
                    return Response(
                        {
                            "status": "error",
                            "message": f"{minimum} not found in mileage data."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if maximum not in mileage_data:
                    return Response(
                        {
                            "status": "error",
                            "message": f"{maximum} not found in mileage data."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            raw = calculate_efficiency_table(
                mileage_data=mileage_data,
                distance_km=serializer.validated_data["distance_km"],
                current_fuel_l=serializer.validated_data["current_fuel_l"],
                fuel_price_per_l=float(vehicle.fuel_price),
                net_factor=serializer.validated_data.get("net_factor", 1.0),
                speed_range=serializer.validated_data.get("speed_range"),
            )

            result = format_efficiency_response(
            raw,
            country_code=serializer.validated_data.get(
                "country_code",
                "IN",
            ),
        )

            return Response(
                {
                    "status": "success",
                    "timestamp": timezone.now(),
                    **result,
                },
                status=status.HTTP_200_OK,
            )

        except Vehicle.DoesNotExist:

            return Response(
                {
                    "status": "error",
                    "message": "Vehicle not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:

            logger.exception(e)

            return Response(
                {
                    "status": "error",
                    "message": "Unable to calculate efficiency.",
                    "error": str(e),
                    "timestamp": timezone.now(),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )