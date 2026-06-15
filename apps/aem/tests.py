"""
AEM Tests

Run:

python manage.py test apps.aem
"""

from django.test import TestCase

from apps.aem.services.factor_calculator import (
    calculate_factors,
)

from apps.aem.services.efficiency_calculator import (
    calculate_efficiency_table,
)

from apps.aem.models import (
    PassengerFactor,
    TirePressureFactor,
    UseFactor,
    ACFactor,
    LoadFactor,
)


class AEMFactorCalculatorTests(TestCase):

    def setUp(self):

        PassengerFactor.objects.bulk_create([
            PassengerFactor(occupants=1, factor=1.00),
            PassengerFactor(occupants=2, factor=0.95),
            PassengerFactor(occupants=3, factor=0.90),
            PassengerFactor(occupants=4, factor=0.85),
            PassengerFactor(occupants=5, factor=0.80),
        ])

        TirePressureFactor.objects.bulk_create([
            TirePressureFactor(pressure_percent=100, factor=1.00),
            TirePressureFactor(pressure_percent=90, factor=0.98),
            TirePressureFactor(pressure_percent=80, factor=0.96),
            TirePressureFactor(pressure_percent=70, factor=0.94),
            TirePressureFactor(pressure_percent=60, factor=0.92),
            TirePressureFactor(pressure_percent=50, factor=0.90),
        ])

        UseFactor.objects.bulk_create([
            UseFactor(odometer_km=0, factor=1.00),
            UseFactor(odometer_km=50000, factor=0.96),
            UseFactor(odometer_km=100000, factor=0.92),
            UseFactor(odometer_km=150000, factor=0.88),
            UseFactor(odometer_km=200000, factor=0.84),
            UseFactor(odometer_km=250000, factor=0.80),
        ])

        ACFactor.objects.bulk_create([
            ACFactor(ac_level=0, factor=1.00),
            ACFactor(ac_level=1, factor=0.98),
            ACFactor(ac_level=2, factor=0.97),
            ACFactor(ac_level=3, factor=0.96),
            ACFactor(ac_level=4, factor=0.95),
            ACFactor(ac_level=5, factor=0.94),
        ])

        LoadFactor.objects.bulk_create([
            LoadFactor(load_percent=0, factor=1.00),
            LoadFactor(load_percent=25, factor=0.90),
            LoadFactor(load_percent=50, factor=0.80),
            LoadFactor(load_percent=75, factor=0.70),
            LoadFactor(load_percent=100, factor=0.60),
        ])

    def test_default_net_factor(self):

        result = calculate_factors()

        self.assertEqual(result["net_factor"], 1.0)

    def test_passenger_factor(self):

        result = calculate_factors(passenger_count=3)

        self.assertEqual(
            result["factors"]["passenger"]["value"],
            0.90,
        )

    def test_full_factor(self):

        result = calculate_factors(

            passenger_count=3,

            tire_pressure_avg_percent=90,

            odometer_km=100000,

            ac_level=4,

            load_percent=50,

        )

        expected = round(
            0.90 *
            0.98 *
            0.92 *
            0.95 *
            0.80,
            3,
        )

        self.assertEqual(
            result["net_factor"],
            expected,
        )


class AEMEfficiencyTests(TestCase):

    def setUp(self):

        self.mileage = {

            30: 14,

            40: 16,

            50: 17,

            60: 16,

            70: 14,

            80: 12,

        }

    def test_best_speed(self):

        result = calculate_efficiency_table(

            mileage_data=self.mileage,

            distance_km=200,

            current_fuel_l=20,

            fuel_price_per_l=1.75,

            net_factor=1.0,

        )

        self.assertEqual(

            result["optimal_speed"]["speed_kmh"],

            50,

        )

    def test_factor_affects_mileage(self):

        result = calculate_efficiency_table(

            mileage_data=self.mileage,

            distance_km=100,

            current_fuel_l=20,

            fuel_price_per_l=1.8,

            net_factor=0.5,

        )

        row = next(

            x

            for x in result["efficiency_table"]

            if x["speed_kmh"] == 50

        )

        self.assertEqual(

            row["effective_mileage_kmpl"],

            8.5,

        )

    def test_trip_completion(self):

        result = calculate_efficiency_table(

            mileage_data=self.mileage,

            distance_km=100,

            current_fuel_l=20,

            fuel_price_per_l=1.8,

        )

        possible = [

            x

            for x in result["efficiency_table"]

            if x["can_complete_trip"]

        ]

        self.assertTrue(

            len(possible) > 0

        )