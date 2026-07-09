from django.db import models

class Country(models.Model):
    external_id = models.IntegerField(unique=True, default=0)

    name = models.CharField(max_length=150)

    iso2 = models.CharField(
        max_length=2,
        unique=True,
    )

    iso3 = models.CharField(
        max_length=3,
        blank=True,
    )

    phone_code = models.CharField(
        max_length=10,
        blank=True,
    )

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="states",
    )

    external_id = models.IntegerField(default=0)

    name = models.CharField(max_length=150)

    state_code = models.CharField(
        max_length=20,
        blank=True,
    )

    class Meta:
        unique_together = ("country", "external_id")
        ordering = ["name"]

    def __str__(self):
        return f"{self.country.iso2} - {self.name}"


class City(models.Model):
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="cities",
    )

    external_id = models.IntegerField(default=0)

    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ("state", "external_id")
        ordering = ["name"]

    def __str__(self):
        return self.name