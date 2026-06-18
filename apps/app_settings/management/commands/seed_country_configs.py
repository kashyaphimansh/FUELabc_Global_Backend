from django.core.management.base import BaseCommand
from apps.app_settings.models import CountryConfig

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