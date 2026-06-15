from django.apps import AppConfig


class AemConfig(AppConfig):
    """
    Advanced Efficiency Management (AEM)

    This module provides:
    - Vehicle Efficiency Calculator
    - Net Factor Calculator
    - Fuel Economy Analytics
    - Trip Fuel Cost Estimation
    - Speed Optimization
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.aem"

    verbose_name = "Advanced Efficiency Management"