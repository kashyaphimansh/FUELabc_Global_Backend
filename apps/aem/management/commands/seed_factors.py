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
    (1,  1.00),
    (2,  0.97),
    (3,  0.94),
    (4,  0.91),
    (5,  0.88),
    (6,  0.85),
    (7,  0.82),
    (8,  0.79),
    (9,  0.76),
    (10, 0.73),
    (11, 0.70),
    (12, 0.67),
    (13, 0.64),
    (14, 0.61),
    (15, 0.58),
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
    (0,       1.00),
    (50000,   0.96),
    (100000,  0.92),
    (150000,  0.88),
    (200000,  0.84),
    (250000,  0.80),
    (300000,  0.77),
    (350000,  0.74),
    (400000,  0.71),
    (450000,  0.68),
    (500000,  0.65),
    (600000,  0.60),
    (700000,  0.55),
    (800000,  0.50),
    (900000,  0.46),
    (1000000, 0.42),
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