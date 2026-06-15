from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.responses import APIResponse

COUNTRY_CONFIGS = {

    "US": {
        "country_name": "United States",
        "currency_code": "USD",
        "currency_symbol": "$",
        "distance_unit": "Mile",
        "fuel_volume_unit": "Gallon",
        "fuel_economy_unit": "MPG",
        "fuel_types": [
            "Regular",
            "Midgrade",
            "Premium",
            "Diesel",
        ],
    },

    "CA": {
        "country_name": "Canada",
        "currency_code": "CAD",
        "currency_symbol": "C$",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "KM/L",
        "fuel_types": [
            "Regular",
            "Premium",
            "Diesel",
        ],
    },

    "UK": {
        "country_name": "United Kingdom",
        "currency_code": "GBP",
        "currency_symbol": "£",
        "distance_unit": "Mile",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "MPG",
        "fuel_types": [
            "Petrol",
            "Diesel",
        ],
    },

    "DE": {
        "country_name": "Germany",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "L/100KM",
        "fuel_types": [
            "Petrol",
            "Diesel",
        ],
    },

    "FR": {
        "country_name": "France",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "L/100KM",
        "fuel_types": [
            "Petrol",
            "Diesel",
        ],
    },

    "AU": {
        "country_name": "Australia",
        "currency_code": "AUD",
        "currency_symbol": "A$",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "KM/L",
        "fuel_types": [
            "Unleaded",
            "Premium",
            "Diesel",
        ],
    },

    "NZ": {
        "country_name": "New Zealand",
        "currency_code": "NZD",
        "currency_symbol": "NZ$",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "KM/L",
        "fuel_types": [
            "91",
            "95",
            "Diesel",
        ],
    },

    "SG": {
        "country_name": "Singapore",
        "currency_code": "SGD",
        "currency_symbol": "S$",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "KM/L",
        "fuel_types": [
            "92",
            "95",
            "98",
            "Diesel",
        ],
    },

    "AE": {
        "country_name": "United Arab Emirates",
        "currency_code": "AED",
        "currency_symbol": "AED",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "KM/L",
        "fuel_types": [
            "Special 95",
            "Super 98",
            "Diesel",
        ],
    },

    "SA": {
        "country_name": "Saudi Arabia",
        "currency_code": "SAR",
        "currency_symbol": "SAR",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "KM/L",
        "fuel_types": [
            "91",
            "95",
            "Diesel",
        ],
    },

    "BR": {
        "country_name": "Brazil",
        "currency_code": "BRL",
        "currency_symbol": "R$",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "KM/L",
        "fuel_types": [
            "Gasoline",
            "Ethanol",
            "Diesel",
        ],
    },

    "MX": {
        "country_name": "Mexico",
        "currency_code": "MXN",
        "currency_symbol": "$",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "KM/L",
        "fuel_types": [
            "Regular",
            "Premium",
            "Diesel",
        ],
    },
}

class SettingsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        country_code = request.user.country_code or "US"

        config = COUNTRY_CONFIGS.get(
            country_code,
            COUNTRY_CONFIGS["US"]
        )

        return APIResponse.success(
            data={
                "country_code": country_code,
                **config,
            }
        )