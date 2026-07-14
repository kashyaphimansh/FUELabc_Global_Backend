from rest_framework import serializers
from .models import CustomerSupport

class CustomerSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupport
        fields = [
            "id",
            "message",
            "is_resolved",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "is_resolved",
        ]