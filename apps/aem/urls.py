"""
AEM URLs

Adaptive Efficiency Model API Routes
"""

from django.urls import path

from .views import (
    FactorCalculatorAPIView,
    EfficiencyCalculatorAPIView,
)

app_name = "aem"

urlpatterns = [

    # ==========================================================
    # Factor Calculator
    # ==========================================================

    path(
        "factors/calculate/",
        FactorCalculatorAPIView.as_view(),
        name="factor-calculator",
    ),

    # ==========================================================
    # Efficiency Calculator
    # ==========================================================

    path(
        "efficiency/calculate/",
        EfficiencyCalculatorAPIView.as_view(),
        name="efficiency-calculator",
    ),
]