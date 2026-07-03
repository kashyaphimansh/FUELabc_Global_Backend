import json
from pathlib import Path

from django.core.management.base import BaseCommand

from apps.location.models import Country, State, City

class Command(BaseCommand):
    help = "Import Countries, States & Cities"

    def handle(self, *args, **kwargs):

        file_path = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "data"
            / "countries+states+cities.json"
        )

        with open(file_path, "r", encoding="utf-8") as f:
            countries = json.load(f)

        City.objects.all().delete()
        State.objects.all().delete()
        Country.objects.all().delete()

        country_count = 0
        state_count = 0
        city_count = 0

        for c in countries:

            country = Country.objects.create(
                external_id=c["id"],
                name=c["name"],
                iso2=c["iso2"],
                iso3=c.get("iso3", ""),
                phone_code=c.get("phonecode", ""),
            )

            country_count += 1

            for s in c.get("states", []):

                state = State.objects.create(
                    country=country,
                    external_id=s["id"],
                    name=s["name"],
                    state_code=s.get("iso2", ""),
                )

                state_count += 1

                cities = [
                    City(
                        external_id=city["id"],
                        state=state,
                        name=city["name"],
                    )
                    for city in s.get("cities", [])
                ]

                City.objects.bulk_create(cities)

                city_count += len(cities)

        self.stdout.write(
            self.style.SUCCESS(
                f"""
Countries : {country_count}
States    : {state_count}
Cities    : {city_count}

Imported Successfully.
"""
            )
        )