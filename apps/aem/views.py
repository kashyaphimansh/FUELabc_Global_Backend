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

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = EfficiencyRequestSerializer(data=request.data)

        if not serializer.is_valid():
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
            # 1. Raw metric calculation
            raw = calculate_efficiency_table(
                mileage_data=serializer.validated_data["mileage_data"],
                distance_km=serializer.validated_data["distance_km"],
                current_fuel_l=serializer.validated_data["current_fuel_l"],
                fuel_price_per_l=serializer.validated_data["fuel_price_per_l"],
                net_factor=serializer.validated_data.get("net_factor", 1.0),
                speed_range=serializer.validated_data.get("speed_range"),
            )

            # 2. Format into USA/Canada response
            result = format_efficiency_response(raw)

            return Response(
                {
                    "status": "success",
                    "timestamp": timezone.now(),
                    **result,
                },
                status=status.HTTP_200_OK,
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


# """
# AEM API Views

# Adaptive Efficiency Model

# Endpoints

# POST /api/v1/aem/factors/calculate

# POST /api/v1/aem/efficiency/calculate
# """

# import logging

# from django.utils import timezone

# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny

# from .serializers import (
#     EfficiencyRequestSerializer,
#     FactorRequestSerializer,
# )

# from .services.factor_calculator import (
#     calculate_factors,
# )

# from .services.efficiency_calculator import (
#     calculate_efficiency_table,
# )

# logger = logging.getLogger(__name__)


# # ==========================================================
# # Factor Calculator
# # ==========================================================

# class FactorCalculatorAPIView(APIView):

#     permission_classes = [AllowAny]

#     def post(self, request):

#         serializer = FactorRequestSerializer(
#             data=request.data
#         )

#         if not serializer.is_valid():

#             return Response(

#                 {

#                     "success": False,

#                     "message": "Validation failed.",

#                     "errors": serializer.errors,

#                     "timestamp": timezone.now(),

#                 },

#                 status=status.HTTP_400_BAD_REQUEST,

#             )

#         try:

#             result = calculate_factors(
#                 **serializer.validated_data
#             )

#             return Response(

#                 {

#                     "success": True,

#                     "message": "Adaptive efficiency factors calculated successfully.",

#                     "data": result,

#                     "timestamp": timezone.now(),

#                 },

#                 status=status.HTTP_200_OK,

#             )

#         except Exception as e:

#             logger.exception(e)

#             return Response(

#                 {

#                     "success": False,

#                     "message": "Unable to calculate factors.",

#                     "error": str(e),

#                     "timestamp": timezone.now(),

#                 },

#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,

#             )


# # ==========================================================
# # Efficiency Calculator
# # ==========================================================

# from .services.efficiency_calculator import calculate_efficiency_table
# from .services.response_formatter import format_efficiency_response  # ADD THIS

# class EfficiencyCalculatorAPIView(APIView):

#     permission_classes = [AllowAny]

#     def post(self, request):

#         serializer = EfficiencyRequestSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response({
#                 "success": False,
#                 "message": "Validation failed.",
#                 "errors": serializer.errors,
#                 "timestamp": timezone.now(),
#             }, status=400)

#         try:

#             # 1. RAW calculation
#             raw = calculate_efficiency_table(
#                 mileage_data=serializer.validated_data["mileage_data"],
#                 distance_km=serializer.validated_data["distance_km"],
#                 current_fuel_l=serializer.validated_data["current_fuel_l"],
#                 fuel_price_per_l=serializer.validated_data["fuel_price_per_l"],
#                 net_factor=serializer.validated_data.get("net_factor", 1.0),
#                 speed_range=serializer.validated_data.get("speed_range"),
#             )

#             # 2. FORMAT OUTPUT (IMPORTANT FIX)
#             result = format_efficiency_response(raw)

#             return Response({
#                 "status": "success",
#                 "timestamp": timezone.now(),
#                 **result
#             }, status=200)
        
#         except Exception as e:
#             logger.exception(e)
#             return Response({
#                 "success": False,
#                 "message": "Unable to calculate efficiency.",
#                 "error": str(e),
#                 "timestamp": timezone.now(),
#             }, status=500)