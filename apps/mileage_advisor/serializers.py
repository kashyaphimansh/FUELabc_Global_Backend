from rest_framework import serializers
from .models import DrivingProfile


class DrivingProfileInputSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=20, default="India", required=False, allow_blank=True)
    state_name = serializers.CharField(max_length=64, required=False, allow_blank=True)
    fuel_type = serializers.CharField(max_length=20, default="petrol")
    fuel_price = serializers.FloatField(min_value=0.01)
    preferred_speed = serializers.FloatField(min_value=30, max_value=150)
    mileage = serializers.FloatField(min_value=0.1)


class SpeedMileageRowSerializer(serializers.Serializer):
    speed = serializers.IntegerField()
    mileage = serializers.FloatField()
    cost = serializers.FloatField()


class DrivingProfileResultSerializer(serializers.Serializer):
    fuel_price = serializers.FloatField()
    preferred_speed = serializers.FloatField()
    mileage = serializers.FloatField()
    arai_mileage = serializers.FloatField()
    best_speed = serializers.IntegerField()
    cost_at_preferred_speed = serializers.FloatField()
    cost_at_best_speed = serializers.FloatField()
    savings_per_unit = serializers.FloatField()
    table = SpeedMileageRowSerializer(many=True)