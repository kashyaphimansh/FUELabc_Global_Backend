from django.contrib import admin
from .models import CountryConfig, CustomerSupport


@admin.register(CountryConfig)
class CountryConfigAdmin(admin.ModelAdmin):
    list_display = (
        "country_code",
        "country_name",
        "currency_code",
        "is_active",
    )


@admin.register(CustomerSupport)
class CustomerSupportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_name",
        "user_email",
        "short_message",
        "is_resolved",
        "created_at",
    )

    list_filter = (
        "is_resolved",
        "created_at",
    )

    search_fields = (
        "user__name",
        "user__email",
        "message",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "user",
        "message",
        "created_at",
        "updated_at",
    )

    @admin.display(description="Name")
    def user_name(self, obj):
        return getattr(obj.user, "name", "-")

    @admin.display(description="Email")
    def user_email(self, obj):
        return obj.user.email

    @admin.display(description="Message")
    def short_message(self, obj):
        if len(obj.message) > 80:
            return obj.message[:80] + "..."
        return obj.message