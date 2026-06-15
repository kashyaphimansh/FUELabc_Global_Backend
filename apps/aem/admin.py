"""
AEM Admin Configuration

Provides an easy interface to manage all factor tables.
"""

from django.contrib import admin

from .models import (
    PassengerFactor,
    TirePressureFactor,
    UseFactor,
    ACFactor,
    LoadFactor,
)


# ==========================================================
# Base Admin
# ==========================================================

class BaseFactorAdmin(admin.ModelAdmin):
    """
    Shared configuration for all factor models.
    """

    list_per_page = 25

    ordering = ("id",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    save_on_top = True


# ==========================================================
# Passenger Factor
# ==========================================================

@admin.register(PassengerFactor)
class PassengerFactorAdmin(BaseFactorAdmin):

    list_display = (
        "occupants",
        "factor",
        "updated_at",
    )

    list_editable = (
        "factor",
    )

    search_fields = (
        "occupants",
    )

    ordering = (
        "occupants",
    )


# ==========================================================
# Tire Pressure Factor
# ==========================================================

@admin.register(TirePressureFactor)
class TirePressureFactorAdmin(BaseFactorAdmin):

    list_display = (
        "pressure_percent",
        "factor",
        "updated_at",
    )

    list_editable = (
        "factor",
    )

    search_fields = (
        "pressure_percent",
    )

    ordering = (
        "-pressure_percent",
    )


# ==========================================================
# Vehicle Use Factor
# ==========================================================

@admin.register(UseFactor)
class UseFactorAdmin(BaseFactorAdmin):

    list_display = (
        "odometer_km",
        "factor",
        "updated_at",
    )

    list_editable = (
        "factor",
    )

    search_fields = (
        "odometer_km",
    )

    ordering = (
        "odometer_km",
    )


# ==========================================================
# AC Factor
# ==========================================================

@admin.register(ACFactor)
class ACFactorAdmin(BaseFactorAdmin):

    list_display = (
        "ac_level",
        "factor",
        "updated_at",
    )

    list_editable = (
        "factor",
    )

    search_fields = (
        "ac_level",
    )

    ordering = (
        "ac_level",
    )


# ==========================================================
# Load Factor
# ==========================================================

@admin.register(LoadFactor)
class LoadFactorAdmin(BaseFactorAdmin):

    list_display = (
        "load_percent",
        "factor",
        "updated_at",
    )

    list_editable = (
        "factor",
    )

    search_fields = (
        "load_percent",
    )

    ordering = (
        "load_percent",
    )