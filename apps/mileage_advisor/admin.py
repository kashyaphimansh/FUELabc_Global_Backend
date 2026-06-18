from django.contrib import admin

from .models import DrivingProfile


@admin.register(DrivingProfile)
class DrivingProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "fuel_type", "fuel_price", "preferred_speed", "mileage", "updated_at")
    search_fields = ("user__username", "user__email", "state_name")
    list_filter = ("country", "fuel_type")