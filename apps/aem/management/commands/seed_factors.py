"""
Seed initial AEM factor data.

Run:

python manage.py seed_factors
"""

from django.core.management.base import BaseCommand

from apps.aem.models import (
    PassengerFactor,
    TirePressureFactor,
    UseFactor,
    ACFactor,
    LoadFactor,
)


class Command(BaseCommand):
    help = "Seed default Adaptive Efficiency Model factor tables"

    def handle(self, *args, **kwargs):

        self.stdout.write("")
        self.stdout.write("Seeding AEM factor tables...")
        self.stdout.write("")

        # ======================================================
        # Passenger Factor
        # ======================================================

        passenger_data = [

            (1, 1.00),
            (2, 0.95),
            (3, 0.90),
            (4, 0.85),
            (5, 0.80),

        ]

        for occupants, factor in passenger_data:

            PassengerFactor.objects.update_or_create(

                occupants=occupants,

                defaults={

                    "factor": factor,

                },

            )

        self.stdout.write("✓ Passenger factors seeded")

        # ======================================================
        # Tire Pressure
        # ======================================================

        tire_data = [

            (100, 1.00),
            (90, 0.98),
            (80, 0.96),
            (70, 0.94),
            (60, 0.92),
            (50, 0.90),

        ]

        for pressure, factor in tire_data:

            TirePressureFactor.objects.update_or_create(

                pressure_percent=pressure,

                defaults={

                    "factor": factor,

                },

            )

        self.stdout.write("✓ Tire pressure factors seeded")

        # ======================================================
        # Vehicle Use
        # ======================================================

        use_data = [

            (0, 1.00),
            (50000, 0.96),
            (100000, 0.92),
            (150000, 0.88),
            (200000, 0.84),
            (250000, 0.80),

        ]

        for km, factor in use_data:

            UseFactor.objects.update_or_create(

                odometer_km=km,

                defaults={

                    "factor": factor,

                },

            )

        self.stdout.write("✓ Vehicle usage factors seeded")

        # ======================================================
        # Air Conditioning
        # ======================================================

        ac_data = [

            (0, 1.00),
            (1, 0.98),
            (2, 0.97),
            (3, 0.96),
            (4, 0.95),
            (5, 0.94),

        ]

        for level, factor in ac_data:

            ACFactor.objects.update_or_create(

                ac_level=level,

                defaults={

                    "factor": factor,

                },

            )

        self.stdout.write("✓ AC factors seeded")

        # ======================================================
        # Cargo Load
        # ======================================================

        load_data = [

            (0, 1.00),
            (25, 0.90),
            (50, 0.80),
            (75, 0.70),
            (100, 0.60),

        ]

        for load, factor in load_data:

            LoadFactor.objects.update_or_create(

                load_percent=load,

                defaults={

                    "factor": factor,

                },

            )

        self.stdout.write("✓ Cargo load factors seeded")

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "AEM factor tables seeded successfully."
            )
        )