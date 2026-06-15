"""
Trip Analytics Serializers

USA / Canada format:
- Speed   : kmh + mph
- Distance: km  + miles
- Mileage : kmpl + mpg
"""

from django.db.models import Avg
from rest_framework import serializers

from .models import Trip, TripData


# ==========================================================
# Graph Data
# ==========================================================

class TripDataSerializer(serializers.ModelSerializer):

    speed_kmh = serializers.SerializerMethodField()
    speed_mph = serializers.SerializerMethodField()

    def get_speed_kmh(self, obj):
        return round(obj.speed, 1)

    def get_speed_mph(self, obj):
        return round(obj.speed * 0.621371, 1)

    class Meta:
        model = TripData
        fields = ["speed_kmh", "speed_mph", "time"]


# ==========================================================
# Trip History
# ==========================================================

class TripHistorySerializer(serializers.ModelSerializer):

    vehicle_name    = serializers.SerializerMethodField()
    date            = serializers.SerializerMethodField()
    time            = serializers.SerializerMethodField()
    duration        = serializers.SerializerMethodField()
    graph_data      = serializers.SerializerMethodField()
    max_speed       = serializers.SerializerMethodField()
    avg_speed       = serializers.SerializerMethodField()
    distance        = serializers.SerializerMethodField()
    average_mileage = serializers.SerializerMethodField()
    co2_emission    = serializers.SerializerMethodField()
    start_location  = serializers.CharField(read_only=True)
    destination     = serializers.CharField(read_only=True)
    is_ended        = serializers.BooleanField(read_only=True)

    # ----------------------------------------------------------
    # Vehicle Name
    # ----------------------------------------------------------

    def get_vehicle_name(self, obj):
        if obj.is_cycle:
            return "Bicycle"
        if obj.vehicle:
            return f"{obj.vehicle.make} {obj.vehicle.model}"
        return "Unknown Vehicle"

    # ----------------------------------------------------------
    # Date / Time (timestamp)
    # ----------------------------------------------------------

    def get_date(self, obj):
        if obj.start_time:
            return obj.start_time.timestamp()
        return None

    def get_time(self, obj):
        if obj.start_time:
            return obj.start_time.timestamp()
        return None

    # ----------------------------------------------------------
    # Duration (minutes)
    # ----------------------------------------------------------

    def get_duration(self, obj):
        if not obj.is_ended:
            return "trip not ended"
        if obj.start_time and obj.end_time:
            return round(
                (obj.end_time - obj.start_time).total_seconds() / 60
            )
        last = TripData.objects.filter(trip=obj).order_by("-time").first()
        if last:
            return round(last.time / 60)
        return 0

    # ----------------------------------------------------------
    # Speed — kmh + mph
    # ----------------------------------------------------------

    def get_max_speed(self, obj):
        top = TripData.objects.filter(trip=obj).order_by("-speed").first()
        if top:
            kmh = round(top.speed, 1)
            return {
                "kmh": kmh,
                "mph": round(kmh * 0.621371, 1),
            }
        return {"kmh": 0, "mph": 0}

    def get_avg_speed(self, obj):
        agg = TripData.objects.filter(trip=obj).aggregate(Avg("speed"))
        avg = agg.get("speed__avg") or 0
        kmh = round(avg, 1)
        return {
            "kmh": kmh,
            "mph": round(kmh * 0.621371, 1),
        }

    # ----------------------------------------------------------
    # Graph Data
    # ----------------------------------------------------------

    def get_graph_data(self, obj):
        data = TripData.objects.filter(trip=obj).order_by("time")
        return TripDataSerializer(instance=data, many=True).data

    # ----------------------------------------------------------
    # Distance — km + miles
    # ----------------------------------------------------------

    def get_distance(self, obj):
        km = float(obj.distance) if obj.distance else 0.0
        return {
            "km": round(km, 2),
            "miles": round(km * 0.621371, 2),
        }

    # ----------------------------------------------------------
    # Mileage — kmpl + mpg
    # ----------------------------------------------------------

    def get_average_mileage(self, obj):
        if obj.average_mileage is None:
            return None
        kmpl = float(obj.average_mileage)
        return {
            "kmpl": round(kmpl, 2),
            "mpg":  round(kmpl * 2.35214, 2),
        }

    # ----------------------------------------------------------
    # CO2
    # ----------------------------------------------------------

    def get_co2_emission(self, obj):
        if obj.co2_emission is None:
            return None
        return round(float(obj.co2_emission), 2)

    class Meta:
        model = Trip
        fields = [
            "id",
            "vehicle_name",
            "is_cycle",
            "date",
            "time",
            "duration",
            "max_speed",
            "avg_speed",
            "graph_data",
            "distance",
            "start_location",
            "destination",
            "average_mileage",
            "co2_emission",
            "is_ended",
            "trip_type",
        ]