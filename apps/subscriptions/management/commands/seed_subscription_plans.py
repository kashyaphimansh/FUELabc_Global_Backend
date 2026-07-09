from django.core.management.base import BaseCommand
from apps.subscriptions.models import SubscriptionPlan

PLANS = [
    {
        "name": "Basic",
        "code": "basic",
        "price": 0,
        "currency": "USD",
        "duration_days": 36500,
    },
    {
        "name": "Premium Monthly",
        "code": "premium_monthly",
        "price": 4.99,
        "currency": "USD",
        "duration_days": 30,
    },
    {
        "name": "Premium Yearly",
        "code": "premium_yearly",
        "price": 44.99,
        "currency": "USD",
        "duration_days": 365,
    },
]

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        for plan in PLANS:
            SubscriptionPlan.objects.update_or_create(
                code=plan["code"],
                defaults={
                    "name": plan["name"],
                    "price": plan["price"],
                    "currency": plan["currency"],
                    "duration_days": plan["duration_days"],
                    "is_active": True,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(PLANS)} subscription plans."
            )
        )