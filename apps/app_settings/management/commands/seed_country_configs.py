from django.core.management.base import BaseCommand
from apps.app_settings.models import CountryConfig
from django.core.management import call_command

COUNTRY_CONFIGS = {

    "US": {
        "country_name": "United States",
        "dial_code": "+1",
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
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "USD",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "$4.99/month",
                "yearly_display_price": "$44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "CA": {
        "country_name": "Canada",
        "dial_code": "+1",
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
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "CAD",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "C$4.99/month",
                "yearly_display_price": "C$44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "UK": {
        "country_name": "United Kingdom",
        "dial_code": "+44",
        "currency_code": "GBP",
        "currency_symbol": "£",
        "distance_unit": "Mile",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "MPG",
        "fuel_types": [
            "Petrol",
            "Diesel",
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "GBP",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "£4.99/month",
                "yearly_display_price": "£44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "DE": {
        "country_name": "Germany",
        "dial_code": "+49",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "L/100KM",
        "fuel_types": [
            "Petrol",
            "Diesel",
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "EUR",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "€4.99/month",
                "yearly_display_price": "€44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "FR": {
        "country_name": "France",
        "dial_code": "+33",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "distance_unit": "KM",
        "fuel_volume_unit": "Litre",
        "fuel_economy_unit": "L/100KM",
        "fuel_types": [
            "Petrol",
            "Diesel",
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "EUR",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "€4.99/month",
                "yearly_display_price": "€44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "AU": {
        "country_name": "Australia",
        "dial_code": "+61",
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
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "AUD",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "A$4.99/month",
                "yearly_display_price": "A$44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "NZ": {
        "country_name": "New Zealand",
        "dial_code": "+64",
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
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "NZD",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "NZ$4.99/month",
                "yearly_display_price": "NZ$44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "SG": {
        "country_name": "Singapore",
        "dial_code": "+65",
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
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "SGD",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "S$4.99/month",
                "yearly_display_price": "S$44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "AE": {
        "country_name": "United Arab Emirates",
        "dial_code": "+971",
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
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "AED",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "AED4.99/month",
                "yearly_display_price": "AED44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "SA": {
        "country_name": "Saudi Arabia",
        "dial_code": "+966",
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
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "SAR",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "SAR4.99/month",
                "yearly_display_price": "SAR44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "BR": {
        "country_name": "Brazil",
        "dial_code": "+55",
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
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "BRL",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "R$4.99/month",
                "yearly_display_price": "R$44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },

    "MX": {
        "country_name": "Mexico",
        "dial_code": "+52",
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
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "MXN",
            },
            "premium": {
                "monthly_price": 4.99,
                "yearly_price": 44.99,
                "monthly_display_price": "$4.99/month",
                "yearly_display_price": "$44.99/year",
                "description": "Unlock all premium features."
            }
        }
    },
}

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        CountryConfig.objects.all().delete()

        configs = []

        for country_code, config in COUNTRY_CONFIGS.items():

            configs.append(
                CountryConfig(
                    country_code=country_code,
                    country_name=config["country_name"],
                    currency_code=config["currency_code"],
                    currency_symbol=config["currency_symbol"],
                    distance_unit=config["distance_unit"],
                    fuel_volume_unit=config["fuel_volume_unit"],
                    fuel_economy_unit=config["fuel_economy_unit"],
                    fuel_types=config["fuel_types"],
                    subscription_plans=config["subscription_plans"],
                )
            )

        CountryConfig.objects.bulk_create(configs)

        self.stdout.write(
            self.style.SUCCESS(
                f"Inserted {len(configs)} countries."
            )
        )
        call_command("seed_subscription_plans")