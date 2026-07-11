from rest_framework import serializers


class SpeedMileageRowSerializer(serializers.Serializer):
    speed = serializers.FloatField()

    # ICE
    mileage = serializers.FloatField(required=False)
    cost = serializers.FloatField(required=False)

    # EV
    range = serializers.FloatField(required=False)
    energy_consumption = serializers.FloatField(required=False)


class DrivingProfileResultSerializer(serializers.Serializer):
    vehicle_id = serializers.IntegerField()

    fuel_price = serializers.FloatField()
    preferred_speed = serializers.FloatField()
    best_speed = serializers.FloatField()

    # ---------- ICE ----------
    mileage = serializers.FloatField(required=False)
    arai_mileage = serializers.FloatField(required=False)
    cost_at_preferred_speed = serializers.FloatField(required=False)
    savings_per_unit = serializers.FloatField(required=False)

    # ---------- EV ----------
    battery_capacity = serializers.FloatField(required=False)
    claimed_range = serializers.FloatField(required=False)

    # Common
    cost_at_best_speed = serializers.FloatField(required=False)

    table = SpeedMileageRowSerializer(many=True)