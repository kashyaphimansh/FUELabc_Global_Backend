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