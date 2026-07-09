from apps.app_settings.models import CountryConfig

def get_user_entitlements(user):
    try:
        country = CountryConfig.objects.get(
            country_code=user.country_code or "AU"
        )

        return country.subscription_plans.get(
            user.subscription_plan,
            country.subscription_plans.get(
                "basic",
                {"vehicle_limit": 9999}
            )
        )

    except Exception:
        return {
            "vehicle_limit": 9999
        }
