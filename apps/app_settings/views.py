from apps.app_settings.models import CountryConfig
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.responses import APIResponse

class SettingsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        country_code = request.user.country_code or "US"

        config = CountryConfig.objects.filter(
            country_code=country_code
        ).first()

        if not config:
            config = CountryConfig.objects.filter(
                country_code="US"
            ).first()

        return APIResponse.success(
            data={
                "country_code": config.country_code,
                "country_name": config.country_name,
                "currency_code": config.currency_code,
                "currency_symbol": config.currency_symbol,
                "distance_unit": config.distance_unit,
                "fuel_volume_unit": config.fuel_volume_unit,
                "fuel_economy_unit": config.fuel_economy_unit,
                "fuel_types": config.fuel_types,
                "subscription_plans": config.subscription_plans,
            }
        )