from django.contrib import admin

from django.urls import path, include

urlpatterns = [

    path(
        'admin/',
        admin.site.urls,
    ),

    path(
        'api/v1/auth/',
        include(
            'apps.users.urls'
        ),
    ),
    path(
        'api/v1/vehicle/',
        include('apps.vehicles.urls'),
    ),
    path(
        'api/v1/payments/',
        include('apps.subscriptions.urls'),
    ),
    path(
        "api/v1/app-settings/",
        include("apps.app_settings.urls"),
    ),

]
