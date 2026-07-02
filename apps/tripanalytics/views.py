"""
Trip Analytics Views

GET /api/v1/tripanalytics/history/
"""

import logging

from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime

from .models import Trip
from .serializers import TripHistorySerializer

logger = logging.getLogger(__name__)


class TripHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            page      = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("page_size", 5))

            start = (page - 1) * page_size
            end   = start + page_size

            base_qs = Trip.objects.filter(
                user=request.user,
                is_ended=True,
                is_archieved=False,
            ).order_by("-start_time")

            trips       = base_qs[start:end]
            total_trips = base_qs.count()

            serializer = TripHistorySerializer(instance=trips, many=True)

            return Response(
                {
                    "status":      "success",
                    "timestamp":   timezone.now(),
                    "data":        serializer.data,
                    "msg":         "success",
                    "error":       False,
                    "total_trips": total_trips,
                    "page":        page,
                    "page_size":   page_size,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.exception(e)
            return Response(
                {
                    "status":    "error",
                    "data":      "",
                    "msg":       str(e),
                    "error":     True,
                    "timestamp": timezone.now(),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        

class TripSaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            trip = Trip.objects.create(
                user=request.user,
                vehicle_id=request.data.get("vehicle_id"),
                start_time=parse_datetime(request.data.get("start_time", "")),
                end_time=parse_datetime(request.data.get("end_time", "")),
                distance=request.data.get("distance_km", 0.0),
                start_location=request.data.get("start_location", ""),
                destination=request.data.get("destination", ""),
                country_code=request.data.get("country_code", "IN"),
                average_mileage=request.data.get("average_mileage"),
                is_ended=True,
            )
            # Speed samples save karo
            for sample in request.data.get("speed_samples", []):
                TripData.objects.create(
                    trip=trip,
                    speed=sample.get("speed", 0),
                    time=sample.get("time", 0),
                )
            return Response({"status": "success", "trip_id": trip.id}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"status": "error", "message": str(e)}, status=400)