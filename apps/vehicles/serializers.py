from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "category",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["vehicle_type"] = (
            data["vehicle_type"]
            .replace("_", " ")
            .title()
        )

        return data