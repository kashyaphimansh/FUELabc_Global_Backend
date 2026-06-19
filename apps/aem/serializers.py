"""
AEM Request Serializers
"""

from rest_framework import serializers


# ==========================================================
# Efficiency Calculator
# ==========================================================

class EfficiencyRequestSerializer(serializers.Serializer):
    """
    POST /api/v1/aem/efficiency/calculate
    """

    # mileage_data = serializers.DictField(
    #     child=serializers.FloatField(min_value=0.1),
    #     help_text="Speed (km/h) -> Mileage (km/L)"
    # )

    vehicle_id = serializers.IntegerField()

    distance_km = serializers.FloatField(
        min_value=0.1,
        max_value=10000
    )

    current_fuel_l = serializers.FloatField(
        min_value=0.1,
        max_value=500
    )

    # fuel_price_per_l = serializers.FloatField(
    #     min_value=0.01
    # )

    net_factor = serializers.FloatField(
        default=1.0,
        min_value=0.01,
        max_value=1.0
    )

    speed_range = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=2,
        max_length=2,
        required=False
    )

    def validate_speed_range(self, value):

        minimum, maximum = value

        if minimum >= maximum:
            raise serializers.ValidationError(
                "Minimum speed must be smaller than maximum speed."
            )

        return value

    # ------------------------------------------------------

    # def validate_mileage_data(self, value):

    #     if not value:
    #         raise serializers.ValidationError(
    #             "Mileage data cannot be empty."
    #         )

    #     converted = {}

    #     for speed, mileage in value.items():

    #         try:
    #             speed = int(speed)
    #         except Exception:
    #             raise serializers.ValidationError(
    #                 f"Invalid speed key : {speed}"
    #             )

    #         if speed <= 0:
    #             raise serializers.ValidationError(
    #                 "Speed must be greater than zero."
    #             )

    #         if mileage <= 0:
    #             raise serializers.ValidationError(
    #                 "Mileage must be greater than zero."
    #             )

    #         converted[speed] = float(mileage)

    #     return converted

    # ------------------------------------------------------

    # def validate_speed_range(self, value):

    #     minimum, maximum = value

    #     if minimum >= maximum:
    #         raise serializers.ValidationError(
    #             "Minimum speed must be smaller than maximum speed."
    #         )

    #     return value

    # # ------------------------------------------------------

    # def validate(self, attrs):

    #     speed_range = attrs.get("speed_range")

    #     if speed_range:

    #         minimum, maximum = speed_range

    #         if minimum >= maximum:
    #             raise serializers.ValidationError(
    #                 {
    #                     "speed_range":
    #                     "Minimum speed must be smaller than maximum speed."
    #                 }
    #             )

    #     return attrs


# ==========================================================
# Factor Calculator
# ==========================================================

class FactorRequestSerializer(serializers.Serializer):
    """
    POST /api/v1/aem/factors/calculate
    """

    passenger_count = serializers.IntegerField(
        min_value=1,
        max_value=5,
        default=1
    )

    tire_pressure_avg_percent = serializers.IntegerField(
        min_value=50,
        max_value=100,
        default=100
    )

    odometer_km = serializers.IntegerField(
        min_value=0,
        max_value=500000,
        default=0
    )

    ac_level = serializers.IntegerField(
        min_value=0,
        max_value=5,
        default=0
    )

    load_percent = serializers.IntegerField(
        min_value=0,
        max_value=200,
        default=0
    )

    # ------------------------------------------------------

    def validate_load_percent(self, value):

        allowed = [0, 25, 50, 75, 100]

        if value not in allowed:

            value = min(
                allowed,
                key=lambda x: abs(x - value)
            )

        return value