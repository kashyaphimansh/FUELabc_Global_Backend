from django.utils import timezone
from rest_framework.permissions import BasePermission


class HasPremiumAccess(BasePermission):

    def has_permission(
        self,
        request,
        view,
    ):

        if not request.user.is_authenticated:
            return False

        return (
            request.user.subscription_plan != "basic"
            and request.user.subscription_expires_at
            and request.user.subscription_expires_at > timezone.now()
        )