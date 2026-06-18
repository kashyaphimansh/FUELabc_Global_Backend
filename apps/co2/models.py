"""
CO2 Models
"""

from django.db import models


class CO2Equivalent(models.Model):
    """
    Relatable equivalents for CO2 savings.
    e.g. "You saved X trees worth of CO2"
    """

    message_template = models.CharField(
        max_length=500,
        help_text="Use {count} as placeholder. e.g. 'Equal to planting {count} trees'"
    )

    co2_kg_equivalent = models.FloatField(
        help_text="How many kg of CO2 this equivalent represents"
    )

    icon_image = models.ImageField(
        upload_to="co2_equivalents/",
        null=True,
        blank=True,
    )

    priority = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["priority"]
        verbose_name = "CO2 Equivalent"
        verbose_name_plural = "CO2 Equivalents"

    def __str__(self):
        return self.message_template