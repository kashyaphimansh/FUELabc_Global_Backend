from apps.subscriptions.services import get_user_entitlements


def build_user_response(user):

    limits = get_user_entitlements(user)

    return {
        "id": str(user.id),

        "phone": user.phone or "",
        "email": user.email or "",
        "name": user.name or "",
        "country_code": user.country_code,
        "dial_code": user.dial_code,
        "login_provider": user.login_provider or "",

        "is_email_verified": user.is_email_verified,
        "is_phone_verified": user.is_phone_verified,

        "profile_completed": bool(
            (user.name or "").strip()
            and
            (user.email or "").strip()
        ),

        "is_vehicle_setup_done":
            user.is_vehicle_setup_done,

        "subscription_plan":
            user.subscription_plan,

        "subscription_expires_at":
            user.subscription_expires_at,

        "is_premium":
            user.is_premium,

        "trips_used":
            user.trips_used,

        "trip_limit":
            limits["trip_limit"],

        "vehicle_limit":
            limits["vehicle_limit"],
    }