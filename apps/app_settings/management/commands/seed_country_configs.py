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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "mi/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "Regular",
            "Midgrade",
            "Premium",
            "Diesel",
            "Electric"
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "USD",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },

            "premium_monthly": {
                "price": 4.99,
                "currency": "USD",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "$4.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 44.99,
                "currency": "USD",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "$44.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "km/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "Regular",
            "Midgrade",
            "Premium",
            "Diesel",
            "Electric"
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "CAD",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },

            "premium_monthly": {
                "price": 4.99,
                "currency": "CAD",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "C$4.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 44.99,
                "currency": "CAD",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "C$44.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "mi/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "Petrol",
            "Diesel",
            "Electric"
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "GBP",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },
            "premium_monthly": {
                "price": 4.99,
                "currency": "GBP",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "£4.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 44.99,
                "currency": "GBP",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "£44.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "km/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "Petrol",
            "Diesel",
            "Electric"
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "EUR",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },
            "premium_monthly": {
                "price": 4.99,
                "currency": "EUR",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "€4.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 44.99,
                "currency": "EUR",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "€44.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "km/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "Petrol",
            "Diesel",
            "Electric"
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "EUR",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },
            "premium_monthly": {
                "price": 4.99,
                "currency": "EUR",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "€4.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 44.99,
                "currency": "EUR",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "€44.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "km/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "Unleaded",
            "Premium",
            "Diesel",
            "Electric"
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "AUD",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },
            "premium_monthly": {
                "price": 6.99,
                "currency": "AUD",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "A$6.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 64.99,
                "currency": "AUD",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "A$64.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "km/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "91",
            "95",
            "Diesel",
            "Electric"
        ],  
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "NZD",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },
            "premium_monthly": {
                "price": 6.99,
                "currency": "NZD",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "NZ$6.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 64.99,
                "currency": "NZD",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "NZ$64.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "km/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "92",
            "95",
            "98",
            "Diesel",
            "Electric"
        ],  
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "SGD",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },
            "premium_monthly": {
                "price": 5.99,
                "currency": "SGD",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "s$5.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 54.99,
                "currency": "SGD",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "S$54.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "km/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "Special 95",
            "Super 98",
            "Diesel",
            "Electric"
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "AED",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },
            "premium_monthly": {
                "price": 4.99,
                "currency": "AED",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "AED$4.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 44.99,
                "currency": "AED",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "AED$44.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "km/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "91",
            "95",
            "Diesel",
            "Electric"
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "SAR",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },
            "premium_monthly": {
                "price": 4.99,
                "currency": "SAR",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "SAR$4.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 44.99,
                "currency": "SAR",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "SAR$44.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "km/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "Gasoline",
            "Ethanol",
            "Diesel",
            "Electric"
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "BRL",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },
            "premium_monthly": {
                "price": 4.99,
                "currency": "BRL",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "R$4.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 44.99,
                "currency": "BRL",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "R$44.99/year",
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
        "ev_price_unit": "kWh",
        "ev_efficiency_unit": "km/kWh",
        "fuel_price_min": 0,
        "fuel_price_max": 200,
        "ev_price_min": 0,
        "ev_price_max": 50,
        "fuel_efficiency_min": 1,
        "fuel_efficiency_max": 100,
        "ev_efficiency_min": 2,
        "ev_efficiency_max": 12,
        "speed_min": 10,
        "speed_max": 200,
        "yearly_distance_min": 1000,
        "yearly_distance_max": 100000,
        "fuel_types": [
            "Regular",
            "Premium",
            "Diesel",
            "Electric"
        ],
        "subscription_plans": {
            "basic": {
                "name": "Basic",
                "price": 0,
                "currency": "MXN",
                "vehicle_limit": 1,
                "trip_limit": 2,
            },
            "premium_monthly": {
                "price": 4.99,
                "currency": "MXN",
                "vehicle_limit": 3,
                "trip_limit": 15,
                "duration_days": 30,
                "display_price": "$4.99/month",
                "description": "Unlock all premium features."
            },

            "premium_yearly": {
                "price": 44.99,
                "currency": "MXN",
                "vehicle_limit": 5,
                "trip_limit": 180,
                "duration_days": 365,
                "display_price": "$44.99/year",
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
                    ev_price_unit=config["ev_price_unit"],
                    ev_efficiency_unit=config["ev_efficiency_unit"],
                    fuel_price_min=config["fuel_price_min"],
                    fuel_price_max=config["fuel_price_max"],
                    ev_price_min=config["ev_price_min"],
                    ev_price_max=config["ev_price_max"],
                    fuel_efficiency_min=config["fuel_efficiency_min"],
                    fuel_efficiency_max=config["fuel_efficiency_max"],
                    ev_efficiency_min=config["ev_efficiency_min"],
                    ev_efficiency_max=config["ev_efficiency_max"],
                    speed_min=config["speed_min"],
                    speed_max=config["speed_max"],
                    yearly_distance_min=config["yearly_distance_min"],
                    yearly_distance_max=config["yearly_distance_max"],
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
    
