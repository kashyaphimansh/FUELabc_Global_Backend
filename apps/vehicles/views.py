from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Vehicle
from .serializers import VehicleSerializer
from apps.subscriptions.services import get_user_entitlements

class VehicleSetupView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        limits = get_user_entitlements(request.user)

        current_vehicle_count = Vehicle.objects.filter(
            user=request.user
        ).count()

        if current_vehicle_count >= limits["vehicle_limit"]:
            return Response(
                {
                    "success": False,
                    "message": "Vehicle limit reached",
                    "upgrade_required": True
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = VehicleSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        vehicle = serializer.save(
            user=request.user
        )

        request.user.is_vehicle_setup_done = True
        request.user.save()

        return Response(
            {
                "success": True,
                "message": "Vehicle Added",
                "data": VehicleSerializer(vehicle).data
            },
            status=status.HTTP_201_CREATED
        )
        
class VehicleListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        vehicles = Vehicle.objects.filter(
            user=request.user
        ).order_by('-created_at')

        serializer = VehicleSerializer(
            vehicles,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )

class VehicleDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        vehicle = Vehicle.objects.get(
            id=pk,
            user=request.user
        )

        serializer = VehicleSerializer(
            vehicle
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )

class VehicleUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        vehicle = Vehicle.objects.get(
            id=pk,
            user=request.user
        )

        serializer = VehicleSerializer(
            vehicle,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Vehicle Updated",
                "data": serializer.data
            }
        )

class VehicleDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        vehicle = Vehicle.objects.get(
            id=pk,
            user=request.user
        )

        vehicle.delete()

        return Response(
            {
                "success": True,
                "message": "Vehicle Deleted"
            }
        )

