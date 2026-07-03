from django.core.management.base import BaseCommand
from apps.vehicles.models import VehicleCatalog

VEHICLES = {
    "passenger": {
        "hatchback": {
            "Toyota": [
                "Yaris",
                "Corolla Hatch",
            ],
            "Hyundai": [
                "i20",
                "i30",
            ],
            "Volkswagen": [
                "Polo",
                "Golf",
            ],
        },

        "sedan": {
            "Toyota": [
                "Camry",
                "Corolla Sedan",
            ],
            "Mazda": [
                "Mazda3",
                "Mazda6",
            ],
            "Honda": [
                "Civic",
                "Accord",
            ],
        },

        "suv": {
            "Toyota": [
                "RAV4",
                "Kluger",
            ],
            "Mazda": [
                "CX-5",
                "CX-8",
            ],
            "Mitsubishi": [
                "Outlander",
                "Pajero Sport",
            ],
        },
    },

    "commercial": {

        "pickup": {
            "Toyota": [
                "Hilux",
            ],
            "Ford": [
                "Ranger",
            ],
            "Isuzu": [
                "D-Max",
            ],
        },

        "mini_truck": {
            "Isuzu": [
                "NLR",
                "NNR",
            ],
            "Fuso": [
                "Canter",
            ],
        },

        "medium_truck": {
            "Hino": [
                "300 Series",
            ],
            "Isuzu": [
                "FRR",
            ],
            "Fuso": [
                "Fighter",
            ],
        },

        "large_truck": {
            "Volvo": [
                "FH",
            ],
            "Scania": [
                "R Series",
            ],
            "MAN": [
                "TGX",
            ],
        },

        "mini_bus": {
            "Toyota": [
                "Coaster",
            ],
            "Fuso": [
                "Rosa",
            ],
        },

        "full_bus": {
            "Volvo": [
                "B8R",
            ],
            "Scania": [
                "K Series",
            ],
        },
    },

    "two_wheeler": {

        "motorcycle": {
            "Honda": [
                "CB125E",
                "CB500F",
            ],
            "Yamaha": [
                "MT-07",
                "YZF-R3",
            ],
            "Kawasaki": [
                "Ninja 400",
                "Z650",
            ],
        },

        "three_wheeler": {
            "Piaggio": [
                "Ape 50",
                "Ape Xtra",
            ],
        },

        "bicycle": {
            "Giant": [
                "Escape 3",
            ],
            "Trek": [
                "Marlin 5",
            ],
            "Merida": [
                "Big Nine 20",
            ],
        },

        "other": {
            "Polaris": [
                "Sportsman 570",
            ],
            "Can-Am": [
                "Outlander 570",
            ],
            "CFMOTO": [
                "CFORCE 520",
            ],
        },
    },
}


class Command(BaseCommand):
    help = "Seed Australia Vehicle Catalog"

    def handle(self, *args, **options):

        VehicleCatalog.objects.all().delete()

        vehicles = []

        for category, vehicle_types in VEHICLES.items():

            for vehicle_type, makes in vehicle_types.items():

                for make, models in makes.items():

                    for model in models:

                        vehicles.append(
                            VehicleCatalog(
                                category=category,
                                vehicle_type=vehicle_type,
                                make=make,
                                model=model,
                                created_by_admin=True,
                                is_active=True,
                            )
                        )

        VehicleCatalog.objects.bulk_create(
            vehicles,
            ignore_conflicts=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Inserted {len(vehicles)} vehicle catalog records."
            )
        )