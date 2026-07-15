from django.urls import path
from . import admin_views
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "is_read",
        "created_at",
    )

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "send/",
                self.admin_site.admin_view(
                    admin_views.send_notification
                ),
                name="send-notification",
            ),
        ]

        return custom_urls + urls