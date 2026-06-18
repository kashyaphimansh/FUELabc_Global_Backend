from .plan_config import PLAN_CONFIG

def get_user_entitlements(user):
    return PLAN_CONFIG.get(
        user.subscription_plan,
        PLAN_CONFIG["basic"]
    )