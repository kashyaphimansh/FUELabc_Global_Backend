"""
Trip Analytics Views

GET /api/v1/tripanalytics/history/
"""

import logging

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Trip, TripData
from .serializers import TripHistorySerializer
from apps.vehicles.models import Vehicle
from apps.co2.calculator import (
    calculate_co2_emission,
    calculate_co2_saved,
)

logger = logging.getLogger(__name__)


class TripHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            page = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("page_size", 5))

            start = (page - 1) * page_size
            end = start + page_size

            base_qs = Trip.objects.filter(
                user=request.user,
                is_ended=True,
                is_archieved=False,
            ).order_by("-start_time")

            trips = base_qs[start:end]
            total_trips = base_qs.count()

            serializer = TripHistorySerializer(
                instance=trips,
                many=True,
            )

            return Response(
                {
                    "status": "success",
                    "timestamp": timezone.now(),
                    "data": serializer.data,
                    "msg": "success",
                    "error": False,
                    "total_trips": total_trips,
                    "page": page,
                    "page_size": page_size,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.exception(e)

            return Response(
                {
                    "status": "error",
                    "data": "",
                    "msg": str(e),
                    "error": True,
                    "timestamp": timezone.now(),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class TripSaveView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:

            logger.warning("========== TRIP SAVE API HIT ==========")
            logger.warning(request.data)

            # ---------------------------------
            # Distance
            # ---------------------------------
            distance = float(
                request.data.get("distance_km", 0) or 0
            )

            # ---------------------------------
            # Mileage
            # ---------------------------------
            average_mileage = request.data.get(
                "average_mileage"
            )

            average_mileage = (
                float(average_mileage)
                if average_mileage
                else None
            )

            # ---------------------------------
            # Vehicle
            # ---------------------------------
            vehicle = Vehicle.objects.get(
                id=request.data.get("vehicle_id"),
                user=request.user,
            )

            fuel_type = vehicle.fuel_type

            logger.warning(
                f"Vehicle Fuel Type : {fuel_type}"
            )

            # ---------------------------------
            # CO2 Calculation
            # ---------------------------------
            actual_emission = calculate_co2_emission(
                average_mileage,
                fuel_type,
            )

            BASELINE_EMISSION = 192

            co2_saved = calculate_co2_saved(
                actual_emission,
                BASELINE_EMISSION,
                distance,
            )

            logger.warning(
                f"Distance={distance}, "
                f"Mileage={average_mileage}, "
                f"Emission={actual_emission}, "
                f"Saved={co2_saved}"
            )

            # ---------------------------------
            # Save Trip
            # ---------------------------------
            trip = Trip.objects.create(
                user=request.user,
                vehicle=vehicle,
                start_time=parse_datetime(
                    request.data.get("start_time", "")
                ),
                end_time=parse_datetime(
                    request.data.get("end_time", "")
                ),
                distance=distance,
                start_location=request.data.get(
                    "start_location",
                    "",
                ),
                destination=request.data.get(
                    "destination",
                    "",
                ),
                country_code=request.data.get(
                    "country_code",
                    "IN",
                ),
                average_mileage=average_mileage,
                co2_emission=actual_emission,
                co2_saved=co2_saved,
                is_ended=True,
            )

            logger.warning(
                f"Trip Saved Successfully. Trip ID={trip.id}"
            )

            # ---------------------------------
            # Save Speed Samples
            # ---------------------------------
            for sample in request.data.get(
                "speed_samples",
                [],
            ):
                TripData.objects.create(
                    trip=trip,
                    speed=sample.get("speed", 0),
                    time=sample.get("time", 0),
                )

            logger.warning(
                "Speed Samples Saved Successfully"
            )

            return Response(
                {
                    "status": "success",
                    "trip_id": trip.id,
                },
                status=status.HTTP_201_CREATED,
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

            logger.exception("Trip Save Error")

            return Response(
                {
                    "status": "error",
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )