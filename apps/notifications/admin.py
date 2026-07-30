from django.contrib import admin

from .models import Notification
from .utils.fcm import send_push_notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "is_read",
        "created_at",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        obj.updated_by = request.user

        super().save_model(request, obj, form, change)

        if obj.user and obj.user.fcm_token:
            send_push_notification(
                obj.user.fcm_token,
                obj.title,
                obj.body,
            )