from rest_framework import serializers

class SpeedMileageRowSerializer(serializers.Serializer):
    speed = serializers.FloatField()
    mileage = serializers.FloatField()
    cost = serializers.FloatField()


class DrivingProfileResultSerializer(serializers.Serializer):
    fuel_price = serializers.FloatField()
    preferred_speed = serializers.FloatField()
    mileage = serializers.FloatField()
    arai_mileage = serializers.FloatField()
    best_speed = serializers.FloatField()
    cost_at_preferred_speed = serializers.FloatField()
    cost_at_best_speed = serializers.FloatField()
    savings_per_unit = serializers.FloatField()
    table = SpeedMileageRowSerializer(many=True)