from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Count
from django.utils.html import format_html_join

from apps.app_settings.models import CustomerSupport
from apps.subscriptions.models import Payment, UserSubscription
from apps.tripanalytics.models import Trip
from apps.vehicles.models import Vehicle
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = (
            "phone",
            "email",
            "name",
            "country_code",
            "dial_code",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields did not match.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            self.save_m2m()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"


class ReadOnlyInlineMixin:
    extra = 0
    can_delete = False
    show_change_link = False

    def has_add_permission(self, request, obj=None):
        return False


class VehicleInline(ReadOnlyInlineMixin, admin.TabularInline):
    model = Vehicle
    fields = (
        "id",
        "make",
        "model",
        "year",
        "vehicle_type",
        "fuel_type",
        "is_active",
        "created_at",
    )
    readonly_fields = fields
    classes = ("collapse",)


class UserSubscriptionInline(ReadOnlyInlineMixin, admin.TabularInline):
    model = UserSubscription
    fields = (
        "id",
        "plan",
        "status",
        "starts_at",
        "expires_at",
        "created_at",
    )
    readonly_fields = fields
    classes = ("collapse",)


class PaymentInline(ReadOnlyInlineMixin, admin.TabularInline):
    model = Payment
    fields = (
        "id",
        "amount",
        "currency",
        "status",
        "razorpay_order_id",
        "razorpay_payment_id",
        "created_at",
    )
    readonly_fields = fields
    classes = ("collapse",)


class TripInline(ReadOnlyInlineMixin, admin.TabularInline):
    model = Trip
    fields = (
        "id",
        "trip_type",
        "vehicle",
        "distance",
        "average_mileage",
        "co2_emission",
        "is_ended",
        "is_archieved",
        "start_time",
        "end_time",
    )
    readonly_fields = fields
    classes = ("collapse",)


class CustomerSupportInline(ReadOnlyInlineMixin, admin.TabularInline):
    model = CustomerSupport
    fields = (
        "id",
        "message",
        "is_resolved",
        "created_at",
        "updated_at",
    )
    readonly_fields = fields
    classes = ("collapse",)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "id",
        "phone_number",
        "email_address",
        "name",
        "login_provider",
        "is_active",
        "is_staff",
        "is_premium",
        "subscription_plan",
        "vehicle_count",
        "trip_count",
        "support_count",
    )
    list_display_links = ("id", "phone_number", "email_address")
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_phone_verified",
        "is_email_verified",
        "profile_completed",
        "is_vehicle_setup_done",
        "is_premium",
        "subscription_plan",
        "login_provider",
        "country_code",
    )
    search_fields = (
        "phone",
        "email",
        "name",
        "country_code",
        "dial_code",
        "current_session_id",
    )
    ordering = ("id",)
    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = (
        "id",
        "last_login",
        "contact_summary",
        "account_summary",
        "activity_summary",
    )
    inlines = (
        VehicleInline,
        UserSubscriptionInline,
        PaymentInline,
        TripInline,
        CustomerSupportInline,
    )

    fieldsets = (
        (
            "User overview",
            {
                "fields": (
                    "id",
                    "contact_summary",
                    "account_summary",
                    "activity_summary",
                )
            },
        ),
        (
            "Identity and contact",
            {
                "fields": (
                    "name",
                    ("dial_code", "phone"),
                    "email",
                    "country_code",
                    "login_provider",
                )
            },
        ),
        (
            "Verification and onboarding",
            {
                "fields": (
                    "is_phone_verified",
                    "is_email_verified",
                    "profile_completed",
                    "is_vehicle_setup_done",
                )
            },
        ),
        (
            "Subscription and usage",
            {
                "fields": (
                    "subscription_plan",
                    "subscription_expires_at",
                    "is_premium",
                    "trips_used",
                )
            },
        ),
        (
            "Authentication",
            {
                "fields": (
                    "password",
                    "current_session_id",
                    "last_login",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            "Create user",
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "email",
                    "name",
                    "country_code",
                    "dial_code",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            vehicle_total=Count("vehicles", distinct=True),
            trip_total=Count("trips", distinct=True),
            subscription_total=Count("usersubscription", distinct=True),
            payment_total=Count("payment", distinct=True),
            support_total=Count("support_requests", distinct=True),
        )

    @admin.display(description="Phone")
    def phone_number(self, obj):
        if not obj.phone:
            return "-"

        return f"{obj.dial_code or ''} {obj.phone}".strip()

    @admin.display(description="Email")
    def email_address(self, obj):
        return obj.email or "-"

    @admin.display(description="Vehicles")
    def vehicle_count(self, obj):
        return getattr(obj, "vehicle_total", obj.vehicles.count())

    @admin.display(description="Trips")
    def trip_count(self, obj):
        return getattr(obj, "trip_total", obj.trips.count())

    @admin.display(description="Support")
    def support_count(self, obj):
        return getattr(obj, "support_total", obj.support_requests.count())

    @admin.display(description="Contact summary")
    def contact_summary(self, obj):
        if obj is None:
            return "-"

        lines = (
            f"Name: {obj.name or '-'}",
            f"Phone: {self.phone_number(obj)} ({self._yes_no(obj.is_phone_verified)} verified)",
            f"Email: {self.email_address(obj)} ({self._yes_no(obj.is_email_verified)} verified)",
            f"Country: {obj.country_code or '-'}",
            f"Login provider: {obj.login_provider or '-'}",
        )
        return self._line_breaks(lines)

    @admin.display(description="Account summary")
    def account_summary(self, obj):
        if obj is None:
            return "-"

        lines = (
            f"Active: {self._yes_no(obj.is_active)}",
            f"Staff: {self._yes_no(obj.is_staff)}",
            f"Superuser: {self._yes_no(obj.is_superuser)}",
            f"Premium: {self._yes_no(obj.is_premium)}",
            f"Profile completed: {self._yes_no(obj.profile_completed)}",
            f"Vehicle setup done: {self._yes_no(obj.is_vehicle_setup_done)}",
        )
        return self._line_breaks(lines)

    @admin.display(description="Activity summary")
    def activity_summary(self, obj):
        if obj is None:
            return "-"

        lines = (
            f"Vehicles: {self.vehicle_count(obj)}",
            f"Trips: {self.trip_count(obj)}",
            f"Trips used: {obj.trips_used}",
            f"Subscriptions: {getattr(obj, 'subscription_total', obj.usersubscription_set.count())}",
            f"Payments: {getattr(obj, 'payment_total', obj.payment_set.count())}",
            f"Support requests: {self.support_count(obj)}",
        )
        return self._line_breaks(lines)

    def _line_breaks(self, lines):
        return format_html_join("", "{}<br>", ((line,) for line in lines))

    def _yes_no(self, value):
        return "Yes" if value else "No"
