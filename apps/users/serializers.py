from rest_framework import serializers

class SendPhoneOTPSerializer(
    serializers.Serializer
):

    phone = serializers.CharField()


class VerifyPhoneOTPSerializer(
    serializers.Serializer
):

    phone = serializers.CharField()
    otp = serializers.CharField()
    country_code = serializers.CharField(required=False)


class SendEmailOTPSerializer(
    serializers.Serializer
):

    email = serializers.EmailField()


class VerifyEmailOTPSerializer(
    serializers.Serializer
):

    email = serializers.EmailField()

    otp = serializers.CharField()


class SocialLoginSerializer(
    serializers.Serializer
):

    provider = serializers.CharField()

    id_token = serializers.CharField()

from rest_framework import serializers


class UserSettingsSerializer(serializers.Serializer):

    distance_unit = serializers.CharField(required=False)

    fuel_volume_unit = serializers.CharField(required=False)

    fuel_economy_unit = serializers.CharField(required=False)

    ev_price_unit = serializers.CharField(required=False)

    ev_efficiency_unit = serializers.CharField(required=False)